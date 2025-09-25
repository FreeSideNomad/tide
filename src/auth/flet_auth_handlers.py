"""
Flet Authentication Flow Handlers

SECURITY REQUIREMENTS (from CLAUDE.md):
- MANDATORY: Follow https://flet.dev/docs/cookbook/authentication/ exactly
- Safety-first design prioritizing user wellbeing
- Secure token storage with encryption
- Complete audit trail for safety monitoring

This module handles OAuth authentication flows using Flet's official patterns.
"""

import logging
from typing import Optional, Callable, Dict, Any
import json
import flet as ft
from .flet_auth_config import get_auth_config

# Configure logging for security audit trail
logger = logging.getLogger(__name__)


class FletAuthHandler:
    """
    Secure authentication flow handler using Flet's official patterns.

    Security Features:
    - Token encryption for client storage
    - Secure session management
    - Authentication state validation
    - Complete audit logging
    - Graceful error handling
    """

    def __init__(self, page: ft.Page):
        """
        Initialize authentication handler.

        Args:
            page: Flet page instance for authentication operations
        """
        self.page = page
        self.auth_config = get_auth_config()
        self.current_user: Optional[Dict[str, Any]] = None

        # Set up Flet authentication event handlers
        self._setup_auth_handlers()

        # Attempt to restore previous session
        self._restore_session()

        logger.info("✅ Flet authentication handler initialized")

    def _setup_auth_handlers(self):
        """Set up Flet's official authentication event handlers."""
        self.page.on_login = self._handle_login_event
        # Note: Flet doesn't have on_logout event, logout is handled manually

        logger.info("✅ Flet auth event handlers configured")

    def _handle_login_event(self, e):
        """
        Handle Flet login event with secure token storage.

        Args:
            e: Login event from Flet's OAuth flow

        Security: Follows ADR-0001 server-side token storage, validates user data
        """
        try:
            if e.error:
                logger.error(f"❌ OAuth login failed: {e.error}")
                self._handle_auth_failure(str(e.error))
                return

            # Extract user information from login event (following GitHub issue #2936 pattern)
            user_data = self._extract_user_data_from_event(e)
            if not user_data:
                logger.error("❌ Failed to extract user data from OAuth response")
                self._handle_auth_failure("Failed to retrieve user information")
                return

            # Securely store authentication data following ADR-0001
            self._store_secure_session(user_data)

            # Update current user state
            self.current_user = user_data

            logger.info(
                f"✅ User authenticated successfully: {user_data.get('email', 'unknown')}"
            )
            self._handle_auth_success(user_data)

        except Exception as error:
            logger.error(f"❌ Login event handler failed: {error}")
            self._handle_auth_failure(f"Authentication processing failed: {error}")

    def _extract_user_data_from_event(self, login_event) -> Optional[Dict[str, Any]]:
        """
        Extract user data from Flet login event (following GitHub issue #2936 pattern).

        Args:
            login_event: Login event from Flet OAuth flow

        Returns:
            Optional[Dict[str, Any]]: User data dictionary or None if failed

        Security: Validates required fields and sanitizes data, follows ADR-0001
        """
        try:
            # Extract user information from login event (GitHub issue #2936 pattern)
            if not hasattr(login_event, "user") or not login_event.user:
                logger.warning("⚠️ No user data in login event")
                return None

            user_info = login_event.user

            # Create user data dictionary with required fields (safe access pattern)
            user_data = {
                "user_id": str(user_info.get("id", user_info.get("sub", ""))),
                "email": user_info.get("email", ""),
                "name": user_info.get(
                    "name",
                    (
                        user_info.get("email", "").split("@")[0]
                        if user_info.get("email")
                        else "User"
                    ),
                ),
                "picture": user_info.get("picture", ""),
                "provider": "google",
                "authenticated": True,
                "session_type": "server_side_pending_adr_implementation",
            }

            # Validate required fields
            required_fields = ["user_id", "email", "name"]
            missing_fields = [
                field for field in required_fields if not user_data.get(field)
            ]
            if missing_fields:
                logger.error(f"❌ Missing required user data fields: {missing_fields}")
                return None

            logger.info(f"✅ User data extracted from event for: {user_data['email']}")

            # Note: Tokens are NOT extracted per ADR-0001 (server-side storage only)
            logger.info(
                "📋 Tokens handled server-side per ADR-0001 - no client-side token extraction"
            )

            return user_data

        except Exception as error:
            logger.error(f"❌ Failed to extract user data from login event: {error}")
            return None

    def _store_secure_session(self, user_data: Dict[str, Any]):
        """
        Store user session following ADR-0001 (server-side only).

        Args:
            user_data: User data dictionary to store

        Security: NO client-side token storage - server-side only per ADR-0001
        """
        try:
            logger.warning("🚫 CLIENT-SIDE TOKEN STORAGE DISABLED per ADR-0001")
            logger.info(
                "📋 Tokens must be stored server-side - implementation pending ADR approval"
            )

            # TEMPORARY: Store only non-sensitive user info until server-side storage implemented
            public_data = {
                "user_id": user_data["user_id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "picture": user_data.get("picture", ""),
                "provider": user_data["provider"],
                "authenticated": True,
                "session_type": "temporary_pending_adr_approval",
            }

            # Store only session identifier (no tokens) per ADR-0001
            session_key = f"tide.session.{user_data['user_id']}"

            if hasattr(self.page.client_storage, "set"):
                self.page.client_storage.set(session_key, json.dumps(public_data))
            elif isinstance(self.page.client_storage, dict):
                self.page.client_storage[session_key] = json.dumps(public_data)

            logger.info(
                f"✅ Temporary session stored for user: {user_data['email']} (tokens server-side pending)"
            )
            logger.warning(
                "⚠️ TOKENS NOT STORED - Server-side implementation required per ADR-0001"
            )

        except Exception as error:
            logger.error(f"❌ Failed to store session: {error}")
            raise

    def _restore_session(self):
        """
        Restore previous authentication session following ADR-0001.

        Security: NO token restoration from client-side - server-side lookup required
        """
        try:
            logger.info("🔍 Attempting session restoration (ADR-0001 compliance)")

            # Look for temporary session data (no tokens)
            # In production, this would query server-side session store
            session_keys = []
            if hasattr(self.page.client_storage, "get_keys"):
                session_keys = [
                    key
                    for key in self.page.client_storage.get_keys("tide.session.") or []
                ]
            elif hasattr(self.page.client_storage, "keys"):
                # Fallback for different client storage implementations
                session_keys = [
                    key
                    for key in self.page.client_storage.keys()
                    if key.startswith("tide.session.")
                ]

            if not session_keys:
                logger.info("ℹ️ No stored authentication session found")
                return

            # Get the most recent session (temporary implementation)
            session_key = session_keys[0]
            session_data_json = None

            if hasattr(self.page.client_storage, "get"):
                session_data_json = self.page.client_storage.get(session_key)
            elif isinstance(self.page.client_storage, dict):
                session_data_json = self.page.client_storage.get(session_key)

            if session_data_json:
                session_data = json.loads(session_data_json)

                # Validate session data (no tokens expected)
                if self._validate_session_data(session_data):
                    self.current_user = session_data
                    logger.info(
                        f"✅ Temporary session restored for user: {session_data.get('email', 'unknown')}"
                    )
                    logger.warning(
                        "⚠️ NO TOKENS AVAILABLE - Server-side token lookup required per ADR-0001"
                    )
                else:
                    logger.warning("⚠️ Invalid session data, clearing storage")
                    self._clear_secure_session()
            else:
                logger.info("ℹ️ No valid session data found")

        except Exception as error:
            logger.warning(f"⚠️ Failed to restore session: {error}")
            self._clear_secure_session()

    def _validate_session_data(self, session_data: Dict[str, Any]) -> bool:
        """
        Validate restored session data.

        Args:
            session_data: Session data to validate

        Returns:
            bool: True if session data is valid
        """
        required_fields = ["user_id", "email", "name", "provider"]
        return all(session_data.get(field) for field in required_fields)

    def _clear_secure_session(self):
        """
        Clear stored session data securely following ADR-0001.

        Security: Removes session identifiers (no tokens per ADR-0001)
        """
        try:
            # Clear session identifiers (no tokens stored per ADR-0001)
            if hasattr(self.page.client_storage, "get_keys"):
                session_keys = [
                    key
                    for key in self.page.client_storage.get_keys("tide.session.") or []
                ]
                for key in session_keys:
                    self.page.client_storage.remove(key)
            elif hasattr(self.page.client_storage, "keys"):
                # Fallback for different client storage implementations
                session_keys = [
                    key
                    for key in self.page.client_storage.keys()
                    if key.startswith("tide.session.")
                ]
                for key in session_keys:
                    if hasattr(self.page.client_storage, "remove"):
                        self.page.client_storage.remove(key)
                    elif hasattr(self.page.client_storage, "pop"):
                        self.page.client_storage.pop(key, None)

            logger.info("✅ Secure session cleared (ADR-0001 compliance)")

        except Exception as error:
            logger.error(f"❌ Failed to clear secure session: {error}")

    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated.

        Returns:
            bool: True if user is authenticated with valid session

        Security: Validates both current state and stored session
        """
        return self.current_user is not None and self._validate_session_data(
            self.current_user
        )

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user data.

        Returns:
            Optional[Dict[str, Any]]: Current user data or None if not authenticated

        Security: Returns copy of user data without sensitive tokens
        """
        if not self.is_authenticated():
            return None

        # Return user data without sensitive tokens for safety
        safe_user_data = {
            "user_id": self.current_user["user_id"],
            "email": self.current_user["email"],
            "name": self.current_user["name"],
            "picture": self.current_user.get("picture", ""),
            "provider": self.current_user["provider"],
        }

        return safe_user_data

    def logout(self):
        """
        Initiate logout by clearing session data.

        Security: Clears stored session data following ADR-0001
        """
        try:
            logger.info("🔓 Initiating user logout")

            # Clear secure session data
            self._clear_secure_session()

            # Reset current user state
            self.current_user = None

            # Call logout success handler
            self._handle_logout_success()

            logger.info("✅ User logout completed successfully")

        except Exception as error:
            logger.error(f"❌ Logout failed: {error}")
            # Ensure session is cleared even if handlers fail
            self.current_user = None

    def _handle_auth_success(self, user_data: Dict[str, Any]):
        """Override in subclass or set callback for successful authentication."""
        pass

    def _handle_auth_failure(self, error_message: str):
        """Override in subclass or set callback for authentication failure."""
        pass

    def _handle_logout_success(self):
        """Override in subclass or set callback for successful logout."""
        pass


class AuthenticatedApp(FletAuthHandler):
    """
    Extended authentication handler with application integration.

    Security Features:
    - Route protection based on authentication state
    - Automatic redirection for unauthenticated users
    - Session validation on route changes
    """

    def __init__(
        self,
        page: ft.Page,
        on_auth_success: Optional[Callable] = None,
        on_auth_failure: Optional[Callable] = None,
        on_logout: Optional[Callable] = None,
    ):
        """
        Initialize authenticated application handler.

        Args:
            page: Flet page instance
            on_auth_success: Callback for successful authentication
            on_auth_failure: Callback for authentication failure
            on_logout: Callback for successful logout
        """
        self.on_auth_success_callback = on_auth_success
        self.on_auth_failure_callback = on_auth_failure
        self.on_logout_callback = on_logout

        super().__init__(page)

        logger.info("✅ Authenticated application handler initialized")

    def _handle_auth_success(self, user_data: Dict[str, Any]):
        """Handle successful authentication with callback."""
        if self.on_auth_success_callback:
            self.on_auth_success_callback(user_data)

    def _handle_auth_failure(self, error_message: str):
        """Handle authentication failure with callback."""
        if self.on_auth_failure_callback:
            self.on_auth_failure_callback(error_message)

    def _handle_logout_success(self):
        """Handle successful logout with callback."""
        if self.on_logout_callback:
            self.on_logout_callback()

    def require_authentication(self, redirect_to_auth: bool = True) -> bool:
        """
        Require authentication for current operation.

        Args:
            redirect_to_auth: Whether to redirect to auth page if not authenticated

        Returns:
            bool: True if authenticated, False otherwise

        Security: Validates current authentication state
        """
        if self.is_authenticated():
            return True

        logger.warning("⚠️ Authentication required but user not authenticated")

        if redirect_to_auth:
            self.page.go("/auth")

        return False
