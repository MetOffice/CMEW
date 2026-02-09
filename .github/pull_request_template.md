[(C) Crown Copyright 2023-2026, Met Office.]: #
[The LICENSE.md file contains full licensing details.]: #
Closes #<issue_number>.

## PR creation checklist for the _developer_

- [ ] The `<issue_number>` above :point_up: has been replaced with the issue number.
- [ ] `main` has been selected as the base branch.
- [ ] The feature branch name follows the format `<issue_number>_<short_description_of_feature>`.
- [ ] The text of the PR title exactly matches with the text (not including the issue number) of the issue title.
- [ ] Appropriate reviewers have been added to the PR (once it is ready for review).
- [ ] The PR has been assigned to the developer(s).
- [ ] The same labels as on the issue (except for the `good first issue` label) have been added to the PR.
- [ ] The `Climate Model Evaluation Workflow (CMEW)` project has been added to the PR.
- [ ] The appropriate milestone has been added to the PR.

## Definition of Done for the _developer_

- [ ] The change in this PR addresses the above issue / all acceptance criteria have been met.
- [ ] The change in this PR follows the requirements in the [wiki: Developer Guide](https://github.com/MetOffice/CMEW/wiki/Developer-Guide) (including copyrights).
- [ ] The GitHub Actions workflow checks pass.
- [ ] The tests run locally and pass (Note: the tests are not run by the GitHub Actions workflow, see [wiki: Run the tests locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#run-the-tests-locally)).
- Updating the tests (select one of the following):
  - [ ] Tests related to the change have been added or updated.
  - [ ] The change does not require tests to be added or updated.
- Updating the user documentation (i.e. everything in the `doc` directory, including the [Quick Start](https://github.com/MetOffice/CMEW/blob/main/doc/source/user_guide/quick_start.rst) section; select one of the following):
  - [ ] The change in this PR does not require the user documentation to be updated.
  - [ ] The user documentation related to the change has been updated appropriately.
- Building the user documentation ([wiki: Build the documentation locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#build-the-documentation-locally) provides instructions; select one of the following):
  - [ ] The change in this PR does not affect the HTML pages.
  - [ ] The HTML pages show the change as expected.
- Updating the API documentation (e.g. docstrings in Python modules; select one of the following):
  - [ ] The change in this PR does not affect the API documentation.
  - [ ] The API documentation related to the change has been updated appropriately.

## PR creation checklist for the _reviewer_

- [ ] Has `<issue_number>` above :point_up: been replaced with the issue number?
- [ ] Has `main` been selected as the base branch?
- [ ] Does the feature branch name follow the format `<issue_number>_<short_description_of_feature>`?
- [ ] Does the text of the PR title exactly match with the text (not including the issue number) of the issue title?
- [ ] Have appropriate reviewers been added to the PR (once it is ready for review)?
- [ ] Has the PR been assigned to the developer(s)?
- [ ] Have the same labels as on the issue (except for the `good first issue` label) been added to the PR?
- [ ] Has the `Climate Model Evaluation Workflow (CMEW)` project been added to the PR?
- [ ] Has the appropriate milestone been added to the PR?

## Definition of Done for the _reviewer_

- [ ] Does the change in this PR address the above issue / have all acceptance criteria been met?
- [ ] Does the change in this PR follow the requirements in the [wiki: Developer Guide](https://github.com/MetOffice/CMEW/wiki/Developer-Guide) (including copyrights)?
- [ ] Have new tests related to the change been added?
- [ ] Do all the GitHub workflow checks pass?
- [ ] Do all the tests run locally and pass? (Note: the tests are not run by the GitHub workflow, see [wiki: Run the tests locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#run-the-tests-locally))
- [ ] Has the API documentation (e.g. docstrings in Python modules) related to the change been updated appropriately?
- [ ] Has the user documentation (i.e. everything in the `doc` directory) related to the change been updated appropriately, including the [Quick Start](https://github.com/MetOffice/CMEW/blob/main/doc/source/user_guide/quick_start.rst) section?
- [ ] Do the HTML pages render correctly? (See [wiki: Build the documentation locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#build-the-documentation-locally))
