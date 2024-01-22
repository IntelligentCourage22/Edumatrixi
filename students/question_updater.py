# from db_operations import *
# from pathlib import Path
# import os
#
# current_directory = os.getcwd()
# topics = topic_names("math")
#
# for i in topics[:16]:
#    # Specify the relative path to the folder
#    folder_name = f"students\\assets\\math\\{i}"
#    # Combine the current directory with the folder name to get the full path
#    directory_path = os.path.join(current_directory, folder_name)
#    path = Path(directory_path)
#    file_names = [(f.name, f.name[:-4][-1]) for f in path.iterdir() if f.is_file()]
#    for name, answer in file_names:
#        statement = (
#            """INSERT INTO Questions (question_text,answer,topic_id) VALUES (?,?,?)"""
#        )
#        question_text = f"math/{i}/{name}"
#        topicid = topic_id(i)
#        datatuple = (question_text, answer, topicid)
#        db.execute(statement, datatuple)
#        con.commit()
#        print("done")
#
#
# db.execute("SELECT * FROM Questions")
# res = db.fetchall()
# print(res)
#
