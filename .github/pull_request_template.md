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

- [ ] This PR contains **only** the changes needed to meet **all** acceptance criteria.
- [ ] The change in this PR follows the requirements in the [wiki: Developer Guide](https://github.com/MetOffice/CMEW/wiki/Developer-Guide) (including copyrights).
- [ ] The GitHub Actions workflow checks pass.
- [ ] The tests run locally and pass (Note: the tests are not run by the GitHub Actions workflow, see [wiki: Run the tests locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#run-the-tests-locally)).
- Updating the Rose metadata (select one of the following):
  - [ ] Rose metadata related to the change has been added or updated.
  - [ ] The change does not require Rose metadata to be added or updated.
- Rendering the Rose metadata (select one of the following):
  - [ ] The Rose GUI shows the change as expected.
  - [ ] The change in this PR does not affect the Rose GUI.
- Updating the tests (select one of the following):
  - [ ] Tests related to the change have been added or updated.
  - [ ] The change does not require tests to be added or updated.
- Updating the user documentation (i.e. everything in the `doc` directory, including the [Quick Start](https://github.com/MetOffice/CMEW/blob/main/doc/source/user_guide/quick_start.rst) section; select one of the following):
  - [ ] The user documentation related to the change has been updated appropriately.
  - [ ] The change in this PR does not require the user documentation to be updated.
- Rendering the user documentation ([wiki: Build the documentation locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#build-the-documentation-locally) provides instructions; select one of the following):
  - [ ] The HTML pages show the change as expected.
  - [ ] The change in this PR does not affect the HTML pages.
- Updating the API documentation (e.g. docstrings in Python modules; select one of the following):
  - [ ] The API documentation related to the change has been updated appropriately.
  - [ ] The change in this PR does not affect the API documentation.

Copyright and IPR:
| I confirm that all code is my own and that my contributions are not subject to copyright or license restrictions. | **your name(s)** |
| I confirm I have not knowingly violated intellectual property rights (IPR) and have taken [sensible measures to prevent doing so](https://metoffice.github.io/ancil-working-practices/working_practices/developer/licence-attribution.html#ai-assistance-and-attribution), including appropriate [attribution for usage of Generative AI](https://metoffice.github.io/ancil-working-practices/working_practices/developer/licence-attribution.html#ai-assistance-and-attribution). I confirm that this work is my own, and I understand that it is my responsibility to ensure I am not violating others’ IPR.  This includes taking reasonable steps to ensure that all tools used while creating this contribution did not infringe IPR. | **your name(s)** |


## PR creation checklist for the _reviewer_

- [ ] The `<issue_number>` above :point_up: has been replaced with the issue number.
- [ ] `main` has been selected as the base branch.
- [ ] The feature branch name follows the format `<issue_number>_<short_description_of_feature>`.
- [ ] The text of the PR title exactly matches with the text (not including the issue number) of the issue title.
- [ ] Appropriate reviewers have been added to the PR (once it is ready for review).
- [ ] The PR has been assigned to the developer(s).
- [ ] The same labels as on the issue (except for the `good first issue` label) have been added to the PR.
- [ ] The `Climate Model Evaluation Workflow (CMEW)` project has been added to the PR.
- [ ] The appropriate milestone has been added to the PR.

## Definition of Done for the _reviewer_

- [ ] This PR contains **only** the changes needed to meet **all** acceptance criteria.
- [ ] The change in this PR follows the requirements in the [wiki: Developer Guide](https://github.com/MetOffice/CMEW/wiki/Developer-Guide) (including copyrights).
- [ ] The GitHub Actions workflow checks pass.
- [ ] The tests run locally and pass (Note: the tests are not run by the GitHub Actions workflow, see [wiki: Run the tests locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#run-the-tests-locally)).
- Updating the Rose metadata (select one of the following):
  - [ ] Rose metadata related to the change has been added or updated.
  - [ ] The change does not require Rose metadata to be added or updated.
- Rendering the Rose metadata (select one of the following):
  - [ ] The Rose GUI shows the change as expected.
  - [ ] The change in this PR does not affect the Rose GUI.
- Updating the tests (select one of the following):
  - [ ] Tests related to the change have been added or updated.
  - [ ] The change does not require tests to be added or updated.
- Updating the user documentation (i.e. everything in the `doc` directory, including the [Quick Start](https://github.com/MetOffice/CMEW/blob/main/doc/source/user_guide/quick_start.rst) section; select one of the following):
  - [ ] The user documentation related to the change has been updated appropriately.
  - [ ] The change in this PR does not require the user documentation to be updated.
- Rendering the user documentation ([wiki: Build the documentation locally](https://github.com/MetOffice/CMEW/wiki/Detailed-Working-Practices#build-the-documentation-locally) provides instructions; select one of the following):
  - [ ] The HTML pages show the change as expected.
  - [ ] The change in this PR does not affect the HTML pages.
- Updating the API documentation (e.g. docstrings in Python modules; select one of the following):
  - [ ] The API documentation related to the change has been updated appropriately.
  - [ ] The change in this PR does not affect the API documentation.

> [!IMPORTANT]
> - Remember to re-check the Definition of Done after making changes in response to a review.
> - The developer merges the PR.
> - Remember to use the format `#<pull_request_number>: <pull_request_title>` when writing the merge commit message for the pull request, so the pull request number is immediately visible on GitHub, regardless of the length of the pull request title.
