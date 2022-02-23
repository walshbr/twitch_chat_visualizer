import pandas as pd

dirid=""
docid ="v1149579272"
logname=dirid + docid + ".txt"

class ChatStream(object):
    """A chat stream has many message files"""
    def __init__(self, logname):
        self.logname = logname
        self.parsed_log = self.parse_the_log()
        self.selfcount = self.parsed_log['message'].value_counts()
        self.total_rows = self.parsed_log.count
        self.csvname = dirid + docid + "_initialparsed.csv"
        self.df = pd.read_csv(self.csvname)
        self.df.index.names=['msg_num']
        #organize by time
        self.df=self.df.set_index('timecode')
        self.df = self.df[self.df.username != 'Fossabot']
        # 

    def parse_the_log(self):
        raw_log = pd.read_csv(self.logname,header=None,delimiter='\n',error_bad_lines=False,encoding='utf-8')
        raw_log['raw_str']=raw_log[0]
        raw_log1=raw_log['raw_str'].str.split(']', n = 1, expand = True)
        raw_log2=raw_log1[1].str.split('>', n = 1, expand = True)
        parsed_log=pd.concat([raw_log1,raw_log2], axis=1, join='inner')
        parsed_log.columns=['timecode','raw','username','message']
        parsed_log=parsed_log.drop(columns='raw')
        parsed_log['username']=parsed_log['username'].map(lambda x: x.lstrip(' <'))
        parsed_log['timecode']=parsed_log['timecode'].map(lambda x: x.lstrip(' ['))
        parsed_log['timecode']=parsed_log['timecode'].replace({',':':'}, regex=True)
        parsed_log['message']=parsed_log['message'].map(lambda x: x.lstrip(' '))
        parsed_log.index.names=['msg_num']
        parsed_log.to_csv(dirid + docid + "_initialparsed.csv",index=False)
        return parsed_log

def main():
    dirid=""
    docid ="v1149579272"
    logname=dirid + docid + ".txt"
    # would be analysis.ChatStream(logname) from interpreter
    ChatStream(logname)

if __name__ == "__main__":
    main()

# goal is pull everything from the notebook over into this file. and run it like this:
# Usage
# $ python3
# >>> import analysis
# >>> chatstream = analysis.ChatStream()
# to re-import it, use importlib
# >>> import importlib
# >>> importlib.reload(analysis)
# then re-instantiate the class -
# >>> analysis.ChatStream()
