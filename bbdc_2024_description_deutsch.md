# Bremen Big Data Challenge 2024

## Daten Download
Die Daten stehen zum Download bereit: (Dateigröße ca. 125MB; entpackt ca. 650MB).


## Aufgabenstellung
Die Bremen Big Data Challenge 2024 behandelt das Aufgabengebiet der Multi-Klassen Klassifikation. Im Detail geht es darum, anhand von Biosignalen Emotionen und Kontext-Informationen vorherzusagen. Die Daten wurden mittels Smartwatches auf verschiedenen Jobmessen für verschiedene Proband:innen aufgenommen.

Ablauf der Datenaufzeichnung: Die Proband:innen haben während des Besuchs einer Messe eine Smartwatch getragen. Diese hat fortlaufend die Bewegung über einen Beschleunigungssensor mit X, Y und Z Achsen aufgezeichnet. Ebenfalls wurden Photo-Plethysmographie (PPG) Daten erfasst. Aus diesen wurden bereits die Herzrate und die "inter beat intervals" (Ibi) des Herzens berechnet. Während des Messebesuchs hat die Smartwatch zu bestimmten Zeitpunkten die Proband:innen nach deren Emotionen und den entsprechenden Kontext-Informationen abgefragt.

Die Wettkampf-Teilnehmenden erhalten aufgenommene Biosignale für 48+5 Proband:innen (Personenspezifisch + Personenunspezifisch). Die jeweiligen erfassten Daten sind von unterschiedlicher zeitlicher Dauer. Für alle 48 Proband:innen sind für mindestens zwei Zeitpunkte erfasste Emotionen und Kontext-Informationen vorhanden. Für die verbleibenden 5 Proband:innen sind keine Emotionen oder Kontext-Informationen verfügbar. Für weitere Zeitpunkte sind andere aufgezeichnete Biosignale vorhanden. Es existieren vier Klassen für Emotionen ("HAPPY", "RELAXED", "ANGRY" und "SAD") und vier Klassen für Kontext-Informationen ("CONVERSATION", "WALKING", "VIEW_BOOTH" und "OTHER"). Die gegebenen Daten sollen analysiert werden und für weitere Zeitpunkte sollen sowohl Emotionen als auch Kontext-Informationen für die 48 Proband:innen vorhergesagt werden (Personenspezifische Aufgabe).
Die 5 Proband:innen können für Modeltraining genutzt werden, müssen im Student Track jedoch nicht prediziert werden.


## Daten Details
Es existieren insgesamt 3 Dateien:

1. "student_data.csv": Enthält alle Daten, die für die Bearbeitung der BBDC 2024 Aufgabe notwendig sind. Die Details der Daten werden nachfolgend beschrieben:

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
  | engagement | A "1" identifies the timestamp at which the subject started interacting with the smartwatch after being notified by the smartwatch. |

  | hrStatus | Description |
  |---|---|
  | -99 | flush() is called but no data. |
  | -10 | PPG signal is too weak or the user's movement is too much. |
  | -8 | PPG signal is weak or there is a user's movement. |
  | -3 | Wearable is detached. |
  | 0 | Initial heart rate measuring state. |
  | 1 | Successful heart rate measurement. |

2. "student_skeleton.csv": Gibt für alle Proband:innen die Zeitpunkte an, für die Emotionen und Kontext-Information vorhergesagt werden sollen. Diese Datei soll um die entsprechenden Klassen ergänzt ("gefüllt") und im Rahmen des BBDC Wettkampfes für eine Score-Berechnung eingereicht werden.
Hierbei geben True und False an, welche Zellen für die Score-Brechenung gewertet werden. Meist ist es für einen Algorithmus einfacher alle Zellen zu füllen, diese werden dann im Upload entsprechend gefiltert. Anmerkung: es ist nicht immer abwechselnd True und False, siehe Zeile 143.


3. "session_info.csv": Diese Datei enthält die zusätzliche Informationen über die Proband:innen und die Aufnahmen:

  | Feature | Description |
  |---|---|
  | sessionId | Unique subject ID. |
  | duration | Duration of recorded session in milliseconds. |
  | watchId | Watch ID of the smartwatch the subject wore throughout the study. |
  | age | Age of the subject. |
  | gender | Gender of the subject. |
  | fairNumber | Number of the fair -> 1, 2, 3. |


## Abgabe
Die Datei "student_skeleton.csv" is mit den zu vorhersagenden Emotionen und Kontext-Informationen zu füllen. Diese können dann im BBDC 2024 Submission Portal (https://bbdc.csl.uni-bremen.de/submission/) hochgeladen werden. Anschließend wird automatisch der Score berechnet und angezeigt sowie die Platzierung im Leadboard aktualisiert. Der Wert `True` in der Skeletondatei zeigt an, das dieser Wert in das Scoring einfließt. Der Wert `False` zeigt an, dass dieser Wert nicht in das Scoring einfließt. Ihr könnt trotzdem alle Werte einfüllen. In dem folgenden Beisipel wird die erste Emotionsprädiktion gewertet und in der nächsten Zeile nur der Kontext. Dies hängt mit der Natur der zeitlich aufeinanderfolgenden Daten zusammen. Die Anzahl der Zeilen oder die Reihenfolge der `sessionId` und `timestamp` sollten nicht verändert werden.

```
sessionId,timestamp,affect,context
1,1652042,True,False
1,1658301,False,True
1,5914412,True,False
```


## Scoring
Der finale Score wird über die Akkuratheit (ACC) der Vorhersagen für die Emotionen und Kontext-Informationen über alle Proband:innen berechnet, welche in der Skeletondatei markiert sind. Je höher der Score, desto besser. Der minimale Score beträgt 0.0 (0%) und der maximale Score beträgt 1.0 (100%).

$$ Accuracy = \frac{Correctly\ Classified}{All\ Classifications} $$
