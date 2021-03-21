import csv
import pandas as pd
import numpy as np

class DataHolder:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load(self):
        f = open(self.file_path)
        reader = csv.reader(f)
        headers = next(reader, None)
        if set(headers) != {'event_time', 'event_type', 'organisation_name', 'place_name','asset_name', 'asset_type', 'module_id'}:
            print('Reupload the file with correct format')
            return 0
        else:
            self.df = pd.read_csv(self.file_path)


    def process(self):
        self.df['event_time'] = pd.to_datetime(self.df['event_time'])
        self.df['event_day'] = self.df['event_time'].dt.date
        self.df['week_day'] = self.df['event_time'].dt.dayofweek
        week_days={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        self.df['week_day'] = self.df['week_day'].map(week_days)

    def aggregate(self, target, **kargs):
        self.target = target
        if 'data' in kargs.keys():
            tmp = kargs['data'].groupby([self.target, 'event_type']).size().reset_index(level = [1]).rename({0 : 'count'}, axis = 1)
        else:
            tmp = self.df.groupby([self.target, 'event_type']).size().reset_index(level = [1]).rename({0 : 'count'}, axis = 1)
        agg_df = pd.DataFrame()
        agg_df[target] = tmp.index.drop_duplicates()
        agg_df['connected']= list(tmp[tmp['event_type'] == 'Connected']['count'])
        agg_df['disconnected']= list(tmp[tmp['event_type'] == 'Disconnected']['count'])
        agg_df['count'] = agg_df['connected'] + agg_df['disconnected']
        agg_df.set_index(target, inplace = True)
        agg_df.sort_values(by = 'count', inplace = True, ascending = False)
        return agg_df

 
    