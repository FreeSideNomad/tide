"""
FastAPI web server for handling OAuth callbacks and authentication.
Provides endpoints for Google OAuth flow integration with Flet application.
"""

import asyncio
import threading
import uuid
import logging
from typing import Dict, Optional, Any
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import uvicorn
from src.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)
from src.auth.oauth import GoogleOAuthService, CSRFError
from src.services.user_service import UserService
from src.database.models import AuthenticationProvider
from src.database.connection import initialize_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthServer:
    """
    FastAPI server for handling OAuth authentication flow.
    Manages the server lifecycle and provides OAuth callback handling.
    """

    def __init__(self, port: int = 8000):
        self.port = port
        self.app = FastAPI(title="Tide Auth Server")
        self.oauth_service = GoogleOAuthService()
        self.user_service = UserService()
        self.server = None
        self.server_thread = None

        # Store for pending authentication sessions
        self.auth_sessions: Dict[str, Dict[str, Any]] = {}

        # Store completed authentication results
        self.auth_results: Dict[str, Dict[str, Any]] = {}

        # Initialize database on startup
        try:
            initialize_database()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")

        self._setup_routes()

    def _setup_routes(self):
        """Set up FastAPI routes for OAuth flow."""

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "tide-auth"}

        @self.app.get("/auth/google/callback")
        async def google_callback(request: Request):
            """Handle Google OAuth callback."""
            logger.info("🔄 OAuth callback received!")
            logger.info(f"Request URL: {request.url}")
            logger.info(f"Query params: {dict(request.query_params)}")

            try:
                # Extract parameters from callback
                code = request.query_params.get("code")
                state = request.query_params.get("state")
                error = request.query_params.get("error")

                logger.info(f"Code present: {bool(code)}")
                logger.info(f"State: {state}")
                logger.info(f"Error: {error}")

                if error:
                    logger.error(f"OAuth error received: {error}")
                    return HTMLResponse(
                        content=self._create_error_page(f"OAuth error: {error}"),
                        status_code=400,
                    )

                if not code or not state:
                    logger.error(
                        f"Missing parameters - code: {bool(code)}, state: {bool(state)}"
                    )
                    return HTMLResponse(
                        content=self._create_error_page(
                            "Missing authorization code or state"
                        ),
                        status_code=400,
                    )

                # Find the corresponding auth session
                logger.info(f"Looking for session with state: {state}")
                logger.info(f"Active sessions: {list(self.auth_sessions.keys())}")

                session_data = None
                for session_id, session in self.auth_sessions.items():
                    logger.info(
                        f"Checking session {session_id}: {session.get('state')}"
                    )
                    if session.get("state") == state:
                        session_data = session
                        logger.info(f"✅ Found matching session: {session_id}")
                        break

                if not session_data:
                    logger.error("❌ No matching session found for state")
                    return HTMLResponse(
                        content=self._create_error_page(
                            "Invalid or expired authentication session"
                        ),
                        status_code=400,
                    )

                # Validate state parameter
                expected_state = session_data["state"]
                logger.info(
                    f"Validating state - received: {state}, expected: {expected_state}"
                )
                if not self.oauth_service.validate_state(state, expected_state):
                    logger.error("❌ State validation failed")
                    raise CSRFError("Invalid state parameter")

                logger.info("✅ State validation passed")

                # Exchange code for tokens
                logger.info("🔄 Exchanging code for tokens...")
                oauth_user_info = await self._exchange_code_for_tokens(code)
                logger.info(
                    f"✅ Got OAuth user info: {oauth_user_info.get('name', 'Unknown')}"
                )

                # Create or retrieve user profile in database
                logger.info("🔄 Creating/retrieving user profile in database...")
                try:
                    user, is_new_user = self.user_service.get_or_create_user_from_oauth(
                        oauth_user_info, AuthenticationProvider.GOOGLE
                    )

                    if is_new_user:
                        logger.info(
                            f"✅ Created new user profile: {user.user_id} ({user.email_address})"
                        )
                    else:
                        logger.info(
                            f"✅ Retrieved existing user profile: {user.user_id} ({user.email_address})"
                        )

                    # Prepare user info for session (combine OAuth and database data)
                    user_info = {
                        "user_id": user.user_id,
                        "email": user.email_address,
                        "name": user.display_name,
                        "picture": user.profile_image_url,
                        "provider": user.authentication_provider.value,
                        "is_new_user": is_new_user,
                        "last_active": (
                            user.last_active_date.isoformat()
                            if user.last_active_date
                            else None
                        ),
                    }

                except ValueError as e:
                    logger.error(f"❌ Failed to create/retrieve user profile: {e}")
                    return HTMLResponse(
                        content=self._create_error_page(
                            f"User profile error: {str(e)}"
                        ),
                        status_code=500,
                    )
                except Exception as e:
                    logger.error(
                        f"❌ Unexpected error during user profile creation: {e}"
                    )
                    return HTMLResponse(
                        content=self._create_error_page(
                            "An unexpected error occurred during authentication"
                        ),
                        status_code=500,
                    )

                # Store the result
                session_id = session_data["session_id"]
                self.auth_results[session_id] = {
                    "success": True,
                    "user_info": user_info,
                    "timestamp": asyncio.get_event_loop().time(),
                }
                logger.info(f"✅ Stored auth result for session: {session_id}")

                # Clean up the pending session
                if session_id in self.auth_sessions:
                    del self.auth_sessions[session_id]
                    logger.info(f"🧹 Cleaned up session: {session_id}")

                return HTMLResponse(
                    content=self._create_success_page(user_info.get("name", "User"))
                )

            except CSRFError as e:
                return HTMLResponse(
                    content=self._create_error_page(f"Security error: {str(e)}"),
                    status_code=403,
                )
            except Exception as e:
                return HTMLResponse(
                    content=self._create_error_page(f"Authentication failed: {str(e)}"),
                    status_code=500,
                )

        @self.app.get("/auth/status/{session_id}")
        async def auth_status(session_id: str):
            """Check authentication status for a session."""
            if session_id in self.auth_results:
                result = self.auth_results[session_id]
                # Clean up old results (optional)
                del self.auth_results[session_id]
                return result
            elif session_id in self.auth_sessions:
                return {"success": False, "status": "pending"}
            else:
                return {"success": False, "status": "not_found"}

    async def _exchange_code_for_tokens(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token and user info."""
        token_url = "https://oauth2.googleapis.com/token"

        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI,
        }

        async with httpx.AsyncClient() as client:
            # Get access token
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_result = token_response.json()

            access_token = token_result.get("access_token")
            if not access_token:
                raise ValueError("No access token received")

            # Get user info
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}

            userinfo_response = await client.get(userinfo_url, headers=headers)
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()

            return user_info

    def create_auth_session(self, auth_url: str, state: str) -> str:
        """Create a new authentication session."""
        session_id = str(uuid.uuid4())
        self.auth_sessions[session_id] = {
            "session_id": session_id,
            "auth_url": auth_url,
            "state": state,
            "timestamp": (
                asyncio.get_event_loop().time() if asyncio._get_running_loop() else 0
            ),
        }
        logger.info(f"📝 Created auth session: {session_id} with state: {state}")
        logger.info(f"📊 Total active sessions: {len(self.auth_sessions)}")
        return session_id

    def _create_success_page(self, user_name: str) -> str:
        """Create success page HTML."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful - Tide</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    text-align: center;
                    background: rgba(255,255,255,0.1);
                    padding: 2rem;
                    border-radius: 1rem;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                }}
                .checkmark {{
                    font-size: 4rem;
                    color: #4CAF50;
                    margin-bottom: 1rem;
                }}
                h1 {{ margin-bottom: 1rem; }}
                p {{ margin-bottom: 0.5rem; opacity: 0.9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="checkmark">✓</div>
                <h1>Welcome to Tide, {user_name}!</h1>
                <p>Authentication successful.</p>
                <p>You can now close this tab and return to the Tide application.</p>
            </div>
            <script>
                // Multiple methods to close the window for better browser compatibility
                function closeWindow() {{
                    // Method 1: Try standard window.close()
                    try {{
                        window.close();
                    }} catch(e) {{
                        console.log('window.close() failed:', e);
                    }}

                    // Method 2: If still open, try to redirect to about:blank
                    setTimeout(() => {{
                        if (!window.closed) {{
                            window.location.href = 'about:blank';
                        }}
                    }}, 500);

                    // Method 3: As last resort, show a clear message
                    setTimeout(() => {{
                        if (!window.closed) {{
                            document.body.innerHTML = `
                                <div class="container">
                                    <div class="checkmark">✓</div>
                                    <h1>Authentication Complete</h1>
                                    <p><strong>You can now close this tab.</strong></p>
                                    <p>Return to the Tide application to continue.</p>
                                    <button onclick="window.close()" style="
                                        background: #4CAF50;
                                        color: white;
                                        border: none;
                                        padding: 12px 24px;
                                        border-radius: 6px;
                                        font-size: 16px;
                                        cursor: pointer;
                                        margin-top: 20px;
                                    ">Close Tab</button>
                                </div>
                            `;
                        }}
                    }}, 1000);
                }}

                // Try to close immediately when page loads
                document.addEventListener('DOMContentLoaded', function() {{
                    // Show countdown for user awareness
                    let countdown = 3;
                    const countdownEl = document.createElement('p');
                    countdownEl.style.fontSize = '14px';
                    countdownEl.style.marginTop = '20px';
                    document.querySelector('.container').appendChild(countdownEl);

                    const updateCountdown = () => {{
                        countdownEl.textContent = `This tab will close automatically in ${{countdown}} seconds...`;
                        countdown--;

                        if (countdown < 0) {{
                            closeWindow();
                        }} else {{
                            setTimeout(updateCountdown, 1000);
                        }}
                    }};

                    updateCountdown();
                }});
            </script>
        </body>
        </html>
        """

    def _create_error_page(self, error_message: str) -> str:
        """Create error page HTML."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Error - Tide</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                }}
                .container {{
                    text-align: center;
                    background: rgba(255,255,255,0.1);
                    padding: 2rem;
                    border-radius: 1rem;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                }}
                .error-icon {{
                    font-size: 4rem;
                    color: #ff6b6b;
                    margin-bottom: 1rem;
                }}
                h1 {{ margin-bottom: 1rem; }}
                p {{ margin-bottom: 0.5rem; opacity: 0.9; }}
                .error-details {{
                    background: rgba(0,0,0,0.2);
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-top: 1rem;
                    font-family: monospace;
                    font-size: 0.9rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error-icon">✗</div>
                <h1>Authentication Failed</h1>
                <p>We encountered an error during the sign-in process.</p>
                <div class="error-details">{error_message}</div>
                <p style="margin-top: 1rem;">Please close this tab and try again.</p>
            </div>
        </body>
        </html>
        """

    def start(self):
        """Start the FastAPI server in a background thread."""
        if self.server_thread and self.server_thread.is_alive():
            return  # Server already running

        def run_server():
            config = uvicorn.Config(
                self.app,
                host="0.0.0.0",
                port=self.port,
                log_level="info",
                access_log=False,  # Reduce noise in logs
            )
            self.server = uvicorn.Server(config)
            asyncio.run(self.server.serve())

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        # Give the server a moment to start
        import time

        time.sleep(1)

    def stop(self):
        """Stop the FastAPI server."""
        if self.server:
            self.server.should_exit = True
        if self.server_thread:
            self.server_thread.join(timeout=5)

    def is_running(self) -> bool:
        """Check if the server is running."""
        return self.server_thread and self.server_thread.is_alive()


# Global server instance
_auth_server: Optional[AuthServer] = None


def get_auth_server() -> AuthServer:
    """Get or create the global auth server instance."""
    global _auth_server
    if _auth_server is None:
        _auth_server = AuthServer()
    return _auth_server


def start_auth_server():
    """Start the global auth server."""
    server = get_auth_server()
    if not server.is_running():
        server.start()
    return server


def stop_auth_server():
    """Stop the global auth server."""
    global _auth_server
    if _auth_server:
        _auth_server.stop()
        _auth_server = None
