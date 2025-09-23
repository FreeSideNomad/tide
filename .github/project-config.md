# GitHub Project Configuration

## Manual Setup Required

The following GitHub Project settings need to be configured manually in the GitHub UI:

### 1. Create GitHub Project
1. Go to your repository on GitHub
2. Click on "Projects" tab
3. Click "New project"
4. Choose "Board" layout
5. Name: "Tide Development Board"

### 2. Configure Board Columns
Create these columns in order:
1. **Backlog** - Approved and ready for planning
2. **Ready** - Sized and ready to start (next sprint items)
3. **In Progress** - Currently being worked on
4. **Review** - Awaiting code review or stakeholder approval
5. **Testing** - In QA/testing phase
6. **Done** - Completed and verified

### 3. Configure Swimlanes
1. Enable swimlanes in project settings
2. Group by: Epic labels
3. Show swimlanes for:
   - `epic:user-profile-setup`
   - `epic:dbt-skills`
   - `epic:safety`
   - No epic (for technical tasks and bugs)

### 4. Set WIP Limits
Configure Work In Progress limits:
- **In Progress**: 3 items per developer
- **Review**: 5 items total
- **Testing**: 3 items total

### 5. Configure Automation Rules
Set up these automation rules:

#### When Issue is Created:
- If has label `type:epic` → Move to "Backlog"
- If has label `type:feature` → Move to "Backlog"
- If has label `type:user-story` → Move to "Backlog"
- If has label `type:bug` AND `priority:critical` → Move to "Ready"
- If has label `type:bug` → Move to "Backlog"

#### When Issue Status Changes:
- If issue is assigned → Move to "Ready"
- If PR is opened linking to issue → Move to "In Progress"
- If PR is in review → Move to "Review"
- If issue is closed → Move to "Done"

#### When Labels Change:
- If `status:blocked` added → Add red flag
- If `status:needs-approval` added → Add yellow flag
- If `priority:critical` added → Move to top of column

### 6. Configure Views
Create additional views:
1. **Epic View**: Filter by `type:epic`
2. **Sprint View**: Filter by `status:ready-for-dev` and `status:in-progress`
3. **Bugs View**: Filter by `type:bug`
4. **Backlog View**: Filter by "Backlog" column

### 7. Configure Fields
Add custom fields:
1. **Epic** (Single select): Link to parent epic
2. **Bounded Context** (Single select): User Management, Questionnaire, etc.
3. **Story Points** (Number): Estimation
4. **Sprint** (Text): Sprint identifier

## Automated Configuration Applied

The following has been automatically configured via files in `.github/`:

✅ **Issue Templates**: 6 templates created with domain model integration
✅ **Labels**: Complete label system for types, priorities, epics, contexts
✅ **Template Configuration**: Issue template chooser configured

## Next Steps

After manual setup:
1. Test issue creation with templates
2. Verify labels are applied correctly
3. Test project board automation
4. Create first epic issue for "User Profile Setup"
5. Create feature issues for Google OAuth and Microsoft OAuth
6. Create user story issues for each feature

## Label Management

To apply the labels from `.github/labels.yml`, you can:

1. **Manual**: Go to Issues → Labels and create each label manually
2. **GitHub CLI**: Use `gh label create` commands
3. **Third-party tool**: Use a label sync tool like `github-label-sync`

Example GitHub CLI commands:
```bash
gh label create "type:epic" --color "8B5CF6" --description "High-level business capability spanning multiple features"
gh label create "type:feature" --color "3B82F6" --description "Specific functionality within an epic"
# ... etc for all labels
```

## Project Board URL
Once created, your project board will be accessible at:
`https://github.com/FreeSideNomad/tide/projects/[project-number]`