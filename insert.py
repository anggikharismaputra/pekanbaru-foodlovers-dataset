from models import session, Account, Post, User, Comment
from jsonparser import JSONParser
import time, sys





def main(path):

    
    data = JSONParser(path)

    try:
        #check account duplicates
        if session.query(Account).filter_by(name=data.account_name).first():
            acc = session.query(Account).filter_by(name=data.account_name).first()
        else:
            acc = Account(name=data.account_name)
            session.add(acc)
            
             
        latest_records =  [i.shortcode for i in session.query(Account).filter_by(name=data.account_name).first().posts]     
        filtered_indices = [data.shortcodes.index(s) for s in data.shortcodes if not s in latest_records]


        print(f"{len(filtered_indices)} new posts found in {path}, {len(data.shortcodes)-len(filtered_indices)} duplicates excluded")

        time.sleep(2)


        for n,idx in enumerate(filtered_indices):
            shortcode,caption, comnum, likes, tag_num, video, time_at = data.get_post(idx)['post'].values()
            users_list = [i['owner'] for i in  data.get_post(idx)['comments']]        
            comments_list = [i['text'] for i in  data.get_post(idx)['comments']]
            timestamps_list = [i['time_created'] for i in data.get_post(idx)['comments']]
            
            #check post duplicates
            if session.query(Post).filter_by(shortcode=shortcode).first():
                post = session.query(Post).filter_by(shortcode=shortcode).first()
            else:
                post = Post(caption=caption, tag_num = tag_num, comment_num=comnum, like=likes, video=video, posted_time=time_at, shortcode=shortcode, account_id=acc.id)          
                session.add(post)

            post.account = acc    
    
            talks =  zip(users_list, comments_list, timestamps_list)
            
            for person, typing, at in talks:                
                comment = Comment(text=typing, commented_time=at)

                if session.query(User).filter_by(name=person).first():
                    user = session.query(User).filter_by(name=person).first()
                else:
                    user = User(name=person)
                    session.add(user)

                session.add(comment)
                comment.post  = post
                comment.account = acc
                comment.user = user
            print(len(filtered_indices)-n, "posts remains")
            
        session.commit()
        
    except KeyboardInterrupt:
        answer = input('commit session?[y/n] : ')
        if answer.lower() == 'y':
            session.commit()
        else:
            print('data are not recorded')
            session.rollback()
   
            

if __name__ == "__main__":
    path  = ''.join(sys.argv[1:])

    main(path)
        
        