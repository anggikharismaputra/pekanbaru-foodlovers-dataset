import json, re
from datetime import datetime


class JSONParser():

    def __init__ (self, path):
        with open(path, encoding='utf-8') as j:
            self.post = json.load(j)['GraphImages']         
        self.length = len(self.post)  
        self.account_name = self.post[0]['username']
        self.shortcodes = [self.get_shortcode(i) for i in range(self.length)]

    def get_timestamp(self,idx):
        timestamp  = self.post[idx]['taken_at_timestamp']
        return datetime.fromtimestamp(timestamp)

    def get_caption(self,idx):
        try:
            caption = self.post[idx]['edge_media_to_caption']['edges'][0]['node']['text']
            return caption
        
        except KeyError:
            caption = self.post[idx]['GraphImages'][idx]['comments']['data']
            return caption

        except IndexError:
            return None

    def get_owner(self,idx):
        owner = self.post[idx]['username']
        return owner

    def get_likesnum(self,idx):
        like = self.post[idx]['edge_media_preview_like']['count']
        return like

    def get_commentsnum(self,idx):
        comments = self.post[idx]['edge_media_to_comment']['count']
        return comments

    def get_videoview(self,idx):
        if self.post[idx]['is_video']:
            return self.post[idx]['video_view_count']
        else:
            return None

    def get_shortcode(self,idx):           
        return self.post[idx]['shortcode']

    def get_post(self,idx):
        post = {'shortcode': self.get_shortcode(idx),
        'caption':self.get_caption(idx),
        'comments':self.get_commentsnum(idx), 
        'likes': self.get_likesnum(idx),
        'tag_num':len(self.get_tagged(idx)), 
        'video_viewer':self.get_videoview(idx),
        'time_posted':self.get_timestamp(idx)}
        comments = self.get_chunk(idx)
        return {'post': post, 'comments':comments}

    def get_chunk(self,idx):
        comments_list = []
        chunk = self.post[idx]['comments']['data']
        for comment in chunk:
            timestamp = comment['created_at']
            owner = comment['owner']['username']
            text = comment['text']
            comments_list.append({
                'time_created': datetime.fromtimestamp(timestamp),
                'owner':owner,
                'text':text})
        return comments_list

    def get_tagged(self,idx):
        string = ' '.join([tuple(i.values())[2] for i in self.get_chunk(idx)])
        tagged = re.findall(r'@\S+', string)
        return tagged

        
