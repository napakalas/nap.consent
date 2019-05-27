# nap.consent

Hi! This is the source code of plone **add-on** specifically for PMR website. The aim of this add-on is to **manage survey** to collect **Physiome Model Repository (PMR)**'s user perception and behaviour when searching for information into PMR.  For this purpose **nap.consent** composted of three parts:
 - Consent
 - Feedback collection
 - Data presentation
Further, we will describe the installation process, set up the survey, and survey specification.

## Installation process
These are steps to install on PMR:
 - Edit **buildout.cfg**, add this code inside the file
  ```
    develop = ${testing:develop}
        ...
        src/nap.consent

    ...
    ...

    eggs=
        ...
        nap.consent
  ```
 - Edit **deploy-all.cfg**, add this code inside the file
  ```
      develop =
        ...
        src/nap.consent
  ```
 - Run this code sequentially:
  ```
    # /etc/init.d/pmr2.zeoserver stop
    # /etc/init.d/pmr2.instance stop
    # bin/buildout
    # bin/buildout -c deploy-all.cfg
    # /etc/init.d/pmr2.zeoserver start
    # /etc/init.d/pmr2.instance start
  ```

## Set up the survey
 - Log in as admin, then access Site Setup page
 - Select the add-ons page
 - Activate **Project Consent 1.0**
 - Do Add-on Configuration by selecting **Consent Settings** link
 - You can then setup the survey by specifying:
   - Allow consent?
   - Title
   - Initial invite
 - Save the configuration

## Type of question

## List of question

|  # |                                                                                             Question                                                                                             |   Function  | Question Type |                                                  Answers                                                 | Low             | High           | Location                                           | Prerequisite                                             |
|:--:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------:|:-------------:|:--------------------------------------------------------------------------------------------------------:|-----------------|----------------|----------------------------------------------------|----------------------------------------------------------|
| 0  | Thanks for your feedback. What could we do to improve?                                                                                                                                           | Requirement | Text          | text                                                                                                     |                 |                | any_page general_page searching_list dodument_page | Appear after giving 5 feedbacks,Only one time            |
| 1  | How familiar are you with this website?                                                                                                                                                          | Familiarity | Likert_1      | 0 - 4                                                                                                    | Not familiar    | Very familiar  | general_page                                       | Only one time                                            |
| 2  | How often do you usually access this website in a month?                                                                                                                                         | Familiarity | Multi         | < 5 times 5 - 10 times 11 - 20 times > 20 times                                                          |                 |                | general_page                                       | After 1,Only one time                                    |
| 3  | How familiar you are with the topic you are looking for?                                                                                                                                         | Familiarity | Likert_2      | 0 - 4 the question is not relevant                                                                       | Not familiar    | Very familiar  | browse_page searching_list                         | One per session                                          |
| 4  | In what level, you need a snippet for each model?                                                                                                                                                | Requirement | Likert_2      | 0 - 4 the question is not relevant                                                                       | I don’t need it | I deserve it   | searching_list                                     | Only one time                                            |
| 5  | What kind of information do you required presented by a snippet?                                                                                                                                 | Requirement | Text          | text                                                                                                     |                 |                | searching_list                                     | After 3, if the answer is 2, 3, or 4,Only one time       |
| 6  | In what level, a query suggestion features is useful for you?                                                                                                                                    | Requirement | Likert_1      | 0 - 4                                                                                                    | Not useful      | Very useful    | searching_list                                     | Only one time                                            |
| 7  | Please provide suggestions to improve the presentation of this result list?                                                                                                                      | Requirement | Text          | text                                                                                                     |                 |                | searching_list                                     | Only one time                                            |
| 8  | In what level, you are satisfied with the results list?                                                                                                                                          | Requirement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Not satisfied   | Very satisfied | searching_list                                     | One per session                                          |
| 9  | Regarding your information needs, which link on this page is the most suitable for you?                                                                                                          | Requirement | Multi         | Documentation Model Metadata Model Curation Mathematics Generated Code Cite this model Source View Other |                 |                | file_page                                          | One per session,Random(2)                                |
| 10 | Regarding your information needs, which part on this page is the most suitable for you?                                                                                                          | Requirement | Likert_2      | Model Status Model Structure Schematic Diagram Original Paper Reference,Other                            |                 |                | document_page file_page                            | One per session,Random(2)                                |
| 11 | How relevant is this page to the information you are looking for?                                                                                                                                | Measurement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Not satisfied   | Very satisfied | document_page file_page                            | One per session per page,search_activity_check,Random(4) |
| 12 | If this is the page you are looking for, how fast can you get this page?                                                                                                                         | Measurement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Very slow       | Very fast      | document_page file_page                            | One per session per page,search_activity_check,Random(4) |
| 13 | If this is the page you are looking for, how easy do you get this page?                                                                                                                          | Measurement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Very difficult  | Very easy      | document_page file_page                            | One per session per page,search_activity_check,Random(4) |
| 14 | How easy is it to get your intended information?                                                                                                                                                 | Measurement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Very difficult  | Very easy      | document_page file_page                            | One per session per page,search_activity_check,Random(4) |
| 15 | If you are looking for information using browse facility and if this is the page you are looking for, how easy is it to find information with browsing facilities compared to search facilities? | Measurement | Likert_2      | 0 - 4 the question is not relevant                                                                       | Very difficult  | Very easy      | document_page file_page                            | One per session per page,browse_activity_check           |

