import pandas as pd
import numpy as np
import os

class TimeWindowDatasetGenerator():

    def __init__(self, 
                time_window=10,
                label_feature='affect',
                data_dir_path='task/',
                exclude_after_notification=False,
                exclude_after_engagement=False
                ) -> None:
        self.time_window = time_window
        self.label_feature = label_feature
        self.data_dir_path = data_dir_path
        self.student_data_path = os.path.join(self.data_dir_path, 'student_data.csv')
        self.student_skeleton_path = os.path.join(self.data_dir_path, 'student_skeleton.csv')
        self.session_data_path = os.path.join(self.data_dir_path, 'SessionData-all.csv')
        self.exclude_after_notification = exclude_after_notification
        self.exclude_after_engagement = exclude_after_engagement


    def get_labelled_timewindow_dataframe(self):
        
        df = pd.read_csv(self.student_data_path, low_memory=False)
        time_window_milliseconds = self.time_window*1000

        temp_df_list = []
        previous_label = None
        previous_session_id = 0

        if self.exclude_after_notification:
            notification_indices = df[(df['notification'].notna())].index

        if self.exclude_after_engagement:
            engagement_indices = df[(df['engagement'].notna())].index

        for count, i in enumerate(df[df[self.label_feature].notna()].index):
            
            end_timestamp = df.iloc[i]['timestamp']

            if self.exclude_after_notification:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                end_timestamp = df.iloc[nearest_notification_index]['timestamp']

            if self.exclude_after_engagement:
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[nearest_engagement_index]['timestamp']

            if self.exclude_after_notification and self.exclude_after_engagement:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[min(nearest_notification_index, nearest_engagement_index)]['timestamp']

            start_timestamp = end_timestamp-time_window_milliseconds
            session_id = df.iloc[i]['sessionId']
            label_name = df.iloc[i][self.label_feature]
            
            temp = pd.DataFrame(df[(df['timestamp']>start_timestamp) & 
                                    (df['timestamp']<=end_timestamp) & 
                                    (df['sessionId']==session_id)])
            temp['label_id'] = count+1
            temp['label'] = label_name
            if session_id == previous_session_id:
                temp['previous_label'] = previous_label
            else:
                temp['previous_label'] = None
            temp_df_list.append(temp)

            previous_session_id = session_id
            previous_label = label_name
            
        time_window_df = pd.concat(temp_df_list)

        return time_window_df

    
    def get_prediction_timewindow_dataframe(self):
        
        df = pd.read_csv(self.student_data_path, low_memory=False)
        df_skeleton = pd.read_csv(self.student_skeleton_path)
        time_window_milliseconds = self.time_window*1000

        temp_df_list = []
        previous_label = None
        previous_session_id = 0

        if self.exclude_after_notification:
            notification_indices = df[(df['notification'].notna())].index

        if self.exclude_after_engagement:
            engagement_indices = df[(df['engagement'].notna())].index

        for count, i in enumerate(df_skeleton.index):

            end_timestamp = df_skeleton.iloc[i]['timestamp']

            if self.exclude_after_notification:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                end_timestamp = df.iloc[nearest_notification_index]['timestamp']

            if self.exclude_after_engagement:
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[nearest_engagement_index]['timestamp']

            if self.exclude_after_notification and self.exclude_after_engagement:
                nearest_notification_index = TimeWindowDatasetGenerator._find_nearest_index(notification_indices, i)
                nearest_engagement_index = TimeWindowDatasetGenerator._find_nearest_index(engagement_indices, i)
                end_timestamp = df.iloc[min(nearest_notification_index, nearest_engagement_index)]['timestamp']

            session_id = df_skeleton.iloc[i]['sessionId']
            try:
                label_name = df.iloc[df[(df['sessionId']==session_id) & 
                                        (df[self.label_feature].notna()) & 
                                        (df['timestamp']<=df_skeleton.iloc[i]['timestamp'])].index.max()][self.label_feature]
            except:
                label_name = None

            temp = pd.DataFrame(df[(df['timestamp']>end_timestamp-time_window_milliseconds) & 
                                    (df['timestamp']<=end_timestamp) & 
                                    (df['sessionId']==session_id)])
            temp['pred_id'] = count+1
            if session_id == previous_session_id:
                temp['previous_label'] = previous_label
            else:
                temp['previous_label'] = None
            temp_df_list.append(temp)

            previous_session_id = session_id
            previous_label = label_name

            temp_df_list.append(temp)

        time_window_dataset = pd.concat(temp_df_list)
        
        return time_window_dataset
        


    def _find_nearest_index(index, search_value):
        array = np.asarray(index)
        idx = (np.abs(array - search_value)).argmin()
        return array[idx]
