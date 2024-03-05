# Bremen Big Data Challenge 2024

## Data download
The data is available for download: (file size approx. 125MB; unpacked approx. 650MB).


## Task
The Bremen Big Data Challenge 2024 deals with the task of multi-class classification. In detail, it is about using biosignals to predict emotions and contextual information. The data was recorded using smartwatches at various job fairs for various test subjects.

Data recording process: The test subjects wore a smartwatch while visiting a trade fair. This continuously recorded the movement via an acceleration sensor with X, Y and Z axes. Photo-plethysmography (PPG) data were also collected. The heart rate and the “inter beat intervals” (Ibi) of the heart have already been calculated from these. During the trade fair visit, the smartwatch asked the test subjects about their emotions and the corresponding contextual information at certain points in time.

The competition participants receive recorded biosignals for 48+5 test subjects (person-specific + person-unspecific). The respective data recorded have different durations. Emotions and context information recorded for at least two points in time are available for all 48 test subjects. No emotions or context information are available for the remaining 5 subjects. Other recorded biosignals are available for further time points. There are four classes for emotions ("HAPPY", "RELAXED", "ANGRY" and "SAD") and four classes for context information ("CONVERSATION", "WALKING", "VIEW_BOOTH" and "OTHER"). The given data should be analyzed and both emotions and context information should be predicted for the 48 test subjects for further points in time (person-specific task).
The 5 test subjects can be used for model training, but do not have to be predicated in the student track.


## Data Details
There are a total of 3 files:

1. "student_data.csv": Contains all data necessary for processing the BBDC 2024 task. The details of the data are described below:

   | Feature | Description |
   |---|---|
   | sessionId | Unique subject ID. |
   | timestamp | Relative time reference of the measurement in milliseconds. |
   | hr | Heart rate value in beats per minute calculated from PPG. |
   | hrIbi | Inter beat interval in milliseconds. The Ibi also provides information about the "heart rate variability" (HRV). |
   | hrStatus | Status flag for heart rate measurement -> see below. |
   | ibiStatus | Status flag for Ibi -> 1: bad; 0: good. |
   | x | Accelerometer value on x-axis. |
   | y | Accelerometer value on y-axis. |
   | z | Accelerometer value on z-axis. |
   | ppgValue | PPG green LED's ADC (analog-to-digital) value. |
   | affect | Affect label of the subject. |
   | context | Context label of the subject. |
   | notification | A "1" identifies the timestamp at which the smartwatch notified the subject. |
   | commitment | A "1" identifies the timestamp at which the subject starts interacting with the smartwatch after being notified by the smartwatch. |

   | hrStatus | Description |
   |---|---|
   | -99 | flush() is called but no data. |
   | -10 | PPG signal is too weak or the user's movement is too much. |
   | -8 | PPG signal is weak or there is a user's movement. |
   | -3 | Wearable is detached. |
   | 0 | Initial heart rate measuring state. |
   | 1 | Successful heart rate measurement. |

2. "student_skeleton.csv": Specifies the times for all test subjects for which emotions and context information should be predicted. This file should be supplemented (“filled”) with the corresponding classes and submitted for a score calculation as part of the BBDC competition.
True and False indicate which cells are counted for the score break. It is usually easier for an algorithm to fill all cells; these are then filtered accordingly in the upload. Note: it is not always alternating True and False, see line 143.


3. "session_info.csv": This file contains additional information about the test subjects and the recordings:

   | Feature | Description |
   |---|---|
   | sessionId | Unique subject ID. |
   | duration | Duration of recorded session in milliseconds. |
   | watchId | Watch ID of the smartwatch the subject wore throughout the study. |
   | age | Age of the subject. |
   | gender | Gender of the subject. |
   | fairNumber | Number of the fair -> 1, 2, 3. |


## Submission
The file "student_skeleton.csv" must be filled with the emotions and context information to be predicted. These can then be uploaded to the BBDC 2024 Submission Portal (https://bbdc.csl.uni-bremen.de/submission/). The score is then automatically calculated and displayed and the placement in the leadboard is updated. The value `True` in the skeleton file indicates that this r value is included in the scoring. The value `False` indicates that this value is not included in the scoring. You can still fill in all values. In the following example, the first emotion prediction is evaluated and in the next line only the context. This is due to the nature of the temporally sequential data. The number of lines or the order of the `sessionId` and `timestamp` should not be changed.

```
sessionId,timestamp,affect,context
1,1652042,True,False
1,1658301,False,True
1.5914412,True,False
```


## Scoring
The final score is calculated using the accuracy (ACC) of the predictions for the emotions and contextual information across all subjects marked in the skeleton file. The higher the score, the better. The minimum score is 0.0 (0%) and the maximum score is 1.0 (100%).

$$ Accuracy = \frac{Correctly\ Classified}{All\ Classifications} $$
