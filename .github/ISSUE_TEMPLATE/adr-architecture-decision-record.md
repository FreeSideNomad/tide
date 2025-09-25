---
name: ADR - Architecture Decision Record
about: Create an Architecture Decision Record for security and architecture decisions
title: 'ADR-XXXX: [Decision Title]'
labels: ['priority:critical', 'architecture', 'needs-approval']
assignees: ''
---

# ADR-XXXX: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: 🟡 Proposed (Pending Stakeholder Approval)
**Technical Story**: [Link to GitHub issue or user story that prompted this decision]

## Context

What is the issue that we're seeing that is motivating this decision or change?

[Describe the problem, constraints, and requirements that led to this decision]

## Proposed Decision

What is the change that we're proposing or have agreed to implement?

[Clear statement of the proposed solution]

## Rationale

Why are we making this decision? What are the driving factors?

[Explain the reasoning behind this choice]

## Consequences

What becomes easier or more difficult to do and any risks introduced by this change?

### ✅ Positive Consequences
- [e.g., improvement of quality attribute satisfaction, follows principle, etc.]
- [...]

### ⚠️ Negative Consequences
- [e.g., compromising quality attribute, violates principle, etc.]
- [...]

### 🚨 Risks
- [e.g., security risks, performance impacts, etc.]
- [...]

## Alternatives Considered

What other options did we look at?

### Alternative 1: [Name]
- **Description**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why rejected**: [Reason]

### Alternative 2: [Name]
- **Description**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why rejected**: [Reason]

## Implementation Requirements

Any specific implementation details, dependencies, or constraints.

[Detail what needs to be implemented to realize this decision]

## Validation Criteria

How will we know this decision is working correctly?

- [ ] [Validation criterion 1]
- [ ] [Validation criterion 2]
- [ ] Security review completed
- [ ] Performance testing completed (if applicable)

---

## 🔐 Approval Process

### Required Approvals

This ADR requires approval from:
- [ ] **Product Owner/Stakeholder**: Business requirements and user impact
- [ ] **Technical Lead**: Technical architecture and feasibility
- [ ] **Security Reviewer**: Security implications and compliance
- [ ] **Additional Reviewer**: [Name and role, if applicable]

### How to Approve

**Stakeholders**: Please provide your approval by commenting:
```
**✅ APPROVED** by [Your Name] - [Your Role]
**Date**: [Date]
**Comments**: [Any conditions, notes, or concerns]
```

### Approval Checklist

- [ ] All required stakeholders have provided explicit approval
- [ ] Security implications reviewed and accepted
- [ ] Implementation plan reviewed and approved
- [ ] Validation criteria agreed upon
- [ ] No blocking concerns raised

---

## 🚫 Implementation Authorization

**⚠️ CRITICAL**: Implementation of features dependent on this ADR is **PROHIBITED** until:

1. ✅ All required approvals obtained (checkboxes above completed)
2. ✅ Issue status changed to **Closed** with "Accepted" label
3. ✅ No unresolved blocking concerns

**Current Status**: 🟡 PENDING STAKEHOLDER APPROVAL

---

## 🛡️ Security Impact Assessment

### Security Considerations
- [ ] Data privacy implications assessed
- [ ] Authentication/authorization impacts reviewed
- [ ] Encryption requirements evaluated
- [ ] Compliance requirements (PIPEDA, health information acts) considered
- [ ] Threat model updated (if applicable)

### Safety-First Principles Alignment
- [ ] User safety prioritized over feature completeness
- [ ] Crisis detection capabilities maintained/improved
- [ ] Evidence-based approach followed
- [ ] Human oversight integration preserved
- [ ] Audit trail capabilities maintained

---

## 📚 References

- [Link to related user story or technical story]
- [Link to relevant documentation]
- [Link to research or external resources]
- [Link to related ADRs]

---

**🚨 This ADR follows the safety-first architecture principles outlined in CLAUDE.md and REQUIRES stakeholder approval before any implementation.**