import pandas as pd
import numpy as np

class TimeWindowDatasetGenerator():

    def __init__(self) -> None:
        pass

    def get_labelled_timewindow_dataframe(self, 
                                        student_data_filepath='task/student_data.csv',
                                        time_window=10,
                                        label_feature='affect',
                                        exclude_after_notification=False,
                                        exclude_after_engagement=False
                                        ):
        
        df = pd.read_csv(student_data_filepath, low_memory=False)
        time_window_milliseconds = time_window*1000

        temp_df_list = []

        if exclude_after_notification:
            notification_indices = df[(df['notification'].notna())].index

        if exclude_after_engagement:
            engagement_indices = df[(df['engagement'].notna())].index

        for count, i in enumerate(df[df[label_feature].notna()].index):
            
            end_timestamp = df.iloc[i]['timestamp']

            if exclude_after_notification:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                end_timestamp = df.iloc[nearest_notification_index]['timestamp']

            if exclude_after_engagement:
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[nearest_engagement_index]['timestamp']

            if exclude_after_notification and exclude_after_engagement:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[min(nearest_notification_index, nearest_engagement_index)]['timestamp']

            start_timestamp = end_timestamp-time_window_milliseconds
            session_id = df.iloc[i]['sessionId']
            label_name = df.iloc[i][label_feature]
            
            temp = pd.DataFrame(df[(df['timestamp']>start_timestamp) & 
                                    (df['timestamp']<=end_timestamp) & 
                                    (df['sessionId']==session_id)])
            temp['label_id'] = count+1
            temp['label'] = label_name
            temp_df_list.append(temp)
            
        time_window_df = pd.concat(temp_df_list)

        return time_window_df

    def _find_nearest_index(index, search_value):
        array = np.asarray(index)
        idx = (np.abs(array - search_value)).argmin()
        return array[idx]
