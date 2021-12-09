# data_reader.py
# By: thekraftyman

import pandas as pd
from os import path

class DataEngine:
    '''
    Data interpreter for strengths
    '''

    def __init__( self, datasource ):
        self._index      = -1
        self._datasource = datasource
        self._datadicts  = []
        self._process_data()

    def _process_data( self ):
        '''
        process a given data source.
            data source can be either a path to a csv file
            or a dict with the correct format (see above)
        '''
        if type( self._datasource ) == dict:
            self._process_dict( self._datasource )
        elif type( self._datasource ) == list:
            self._process_list()
        elif type( self._datasource ) == str:
            self._process_file()
        else:
            raise Exception( "Data source not a dict, list of dicts, or file string" )

    def _process_list( self ):
        '''
        take a list of dicts and process for generator
        '''
        for point in self._datasource:
            if type( point ) == dict:
                self._process_dict( point )
            else:
                raise Exception( "Data from list not dictionary" )

    def _process_dict( self, data ):
        '''
        takes a dict and processes it for the generator
        '''
        assert type( data ) == dict
        self._datadicts.append( data )

    def _process_file( self ):
        '''
        Takes a file and processes it for use in the generator
        '''
        self._df = pd.read_csv( self._datasource )
        for i in range( self._df.shape[0] ):
            self._datadicts.append({
                "First Name": self._df.iloc[i,:]['First Name'],
                "Last Name" : self._df.iloc[i,:]['Last Name'],
                "Talent 1"  : self._df.iloc[i,:]['Talent 1'],
                "Talent 2"  : self._df.iloc[i,:]['Talent 2'],
                "Talent 3"  : self._df.iloc[i,:]['Talent 3'],
                "Talent 4"  : self._df.iloc[i,:]['Talent 4'],
                "Talent 5"  : self._df.iloc[i,:]['Talent 5']
            })

    def __len__( self ):
        return len( self._datadicts )

    def __getitem__( self, index ):
        return self._datadicts[ index ]

    def __iter__( self ):
        '''
        iterator for the processed data
        '''
        return self

    def __next__( self ):
        '''
        next step for iterator
        '''
        self._index += 1
        if self._index >= len(self):
            self._index = -1
            raise StopIteration
        else:
            return self._datadicts[ self._index ]
