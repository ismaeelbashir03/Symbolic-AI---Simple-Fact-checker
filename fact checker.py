# this is my first symbolic ai, i am doing this small program to learn more about symbolic ai 
# so i can implement my first neuro symbolic ai later. this program allows you to store facts and 
# use symbolic ai to check if they are true, by checking the knowledge base. (this is a very simple version
# most symbolic ai's will be way more complicated, this is just for my own learning purposes).

# importing libraries needed
import nltk
from nltk.parse import CoreNLPParser
import stanza 
import pickle 
import os

# initialising stanfords stanza text parser
nlp = stanza.Pipeline('en')

# creating classes for each knowledge type by inheriting a main knowledge class
class Knowledge():
    def __init__(self, subject, object, correct):
        self.subject = subject
        self.object = object
        self.correct = correct

    # checks if the fact is true
    def is_correct(self):
        return self.correct

    # checks if subject and object are matching this fact
    def check(self, subject, object):

        if subject == self.subject and object == self.object:
            return True

        else:
            return False

# current fact
class Knowledge_is(Knowledge):
    def __init__(self, subject, object, correct):
        super().__init__(subject, object, correct)
        self.type = "is"

# previous fact
class Knowledge_was(Knowledge):
    def __init__(self, subject, object, correct):
        super().__init__(subject, object, correct)
        self.type = "was"

# memeory of knowledge base so program remembers previous facts
# checking this is first time running, if so we initialise the knowledge base
# with some facts (may be outdated)
if os.path.exists('memory.dat'):

    # reading in our previous knowledge base if we hav ran the progran before
    with open("memory.dat", "rb") as f: 
        knowledge_base = pickle.load(f)

else:
    knowledge_base = [Knowledge_was("obama", "president", True),Knowledge_was("trump", "president", True),Knowledge_is("biden", "president", True)]


# function to answer questions
def answer_question(doc):

    # for each sentence i get the object, subject and aux of the sentence
    for question in doc.sentences:
        # Parsing the question to extract the subject and object
        subject = [str(word.text).lower() for word in question.words if word.upos == 'PROPN']
        statement = [str(word.text).lower() for word in question.words if word.upos == 'AUX']
        object = [str(word.text).lower() for word in question.words if word.upos == 'NOUN']
        
        # checking if at least on of these sentence properties where detected
        if len(subject) != 0 and len(statement) != 0 and len(object) != 0:
            subject = subject[0]
            statement = statement[0]
            object = object[0]
        # if not we ask the user to try again
        else:
            print(f'subjects: {subject}, objects: {object}')
            print("I cant detect a subject or object, please try again.")
        
        # Using symbolic AI to reason about the subject and object and generate an answer
        # checking is this is a current fact
        if 'is' in statement:
            # we loop through our knowledge base and check if its true, we then return an answer
            for k in knowledge_base:
                if k.check(subject, object):
                    if k.correct and k.type == "is":
                        return f"Yes, {subject} is {object}"
                    else:
                        return f"No, {subject} is not {object}"
            
            # if we cannot find anything about our subject and object we ask if this should be added to the knowledge base
            out = ""
            while out != "n" and out != "y":
                out = input(f"No data on {subject} being {object}, should i add this fact to my knowledge base? [y/n]: ").lower()

                if out != "n" and out != "y":
                    print("please andwer yes or no.")
            
            if out == "y":
                isTrue = ""
                while isTrue != "y" and isTrue != "n":
                    isTrue = input(f"is {subject} a {object}? [y/n]: ")

                    if isTrue != "y" and isTrue != "n":
                        print("please answer yes or no.")

                if isTrue == "y":
                    isTrue = True
                elif isTrue == "n":
                    isTrue = False

                add_knowledge(statement, subject, object, isTrue)
                return f"statement: {subject} is {object} added to knowledge base."

        # we do the same but now for previous facts
        elif 'was' in statement:
            for k in knowledge_base:
                if k.check(subject, object):
                    if k.correct and k.type == "was":
                        return f"Yes, {subject} was {object}"
                    else:
                        return f"No, {subject} was not {object}"
            
            # again we ask if we should add the fact if not present in knowledge base
            out = ""
            while out != "n" and out != "y":
                out = input(f"No data on {subject} previously being {object}, should i add this to my knowledge base? [y/n]: ").lower()

                if out != "n" and out != "y":
                    print("please answer yes or no.")
            
            if out == "y":
                isTrue = ""
                while isTrue != "y" and isTrue != "n":
                    isTrue = input(f"is {subject} a {object}? (should i set this statement to true) [y/n]: ")

                    if isTrue != "y" and isTrue != "n":
                        print("please answer yes or no.")

                if isTrue == "y":
                    isTrue = True
                elif isTrue == "n":
                    isTrue = False

                add_knowledge(statement, subject, object, isTrue)
                return f"statement: {subject} is {object} added to knowledge base."
            elif out == "n":
                return ""
        else:
            return f"I don't understand the question, please ask 'is' or 'are' questions."

# here we define how to add a fact to the knowledge base
def add_knowledge(type, subject, object, isTrue):

    # we check the types first
    if type == "is":
        # if the fact added in is a previous fact ebing changed, we remove the old fact and add the new one
        if (any(x.subject == subject and x.object == object and x.correct != isTrue for x in knowledge_base)):
            remove_knowledge(type, subject, object, isTrue)
            knowledge_base.append(Knowledge_is(subject, object, isTrue))
            print("overwritten previous knowledge fact.")
        # if we aleady have the fact in our knowledge base we tell the user and return
        elif (any(x.subject == subject and x.object == object and x.correct == isTrue for x in knowledge_base)):
            print(f"{subject} is {object} already in my knowledge base.")

        # if fact not in knowledge base then we add it
        elif not(any(x.subject == subject and x.object == object and x.correct == isTrue for x in knowledge_base)):
            knowledge_base.append(Knowledge_is(subject, object, isTrue))
            print("knowledge added.")

    # we do the same for a previous fact
    elif type == "was":
        if (any(x.subject == subject and x.object == object and x.correct != isTrue for x in knowledge_base)):
            remove_knowledge(type, subject, object, isTrue)
            knowledge_base.append(Knowledge_was(subject, object, isTrue))
            print("overwritten previous knowledge fact.")
        elif (any(x.subject == subject and x.object == object and x.correct == isTrue for x in knowledge_base)):
            print(f"{subject} is {object} already in my knowledge base.")

        elif not(any(x.subject == subject and x.object == object and x.correct == isTrue for x in knowledge_base)):
            knowledge_base.append(Knowledge_is(subject, object, isTrue))
            print("knowledge added.")

# this is a function to remove fact, this can be used but i decided against implemnenting it, as
# we might aswell change a fact from being true or false than outright removing it
def remove_knowledge(type, subject, object, isTrue):
    rem = 0
    if type == "is":
        for k in knowledge_base:
            if k.object == object and k.subject == subject and k.type == "is":
                rem = k

    elif type == "was":
        for k in knowledge_base:
            if k.object == object and k.subject == subject and k.type == "is":
                rem = k

    if rem == 0:
        print("Data not in memory, cannot delete")
        return

    knowledge_base.remove(rem)

# main loop
done = False
while done == False:
    # asking the user for options for main menu
    q_type = ''
    while q_type != "a" and q_type != "b" and q_type != "c":
        q_type = input("Do you want to add knowledge [A] or ask about knowledge [B] or quit [C]?: ").lower()

        if q_type != "a" and q_type != "b" and q_type != "c":
            print("Please answer 'a' or 'b' or 'c")

    # if we are adding a fact, we take input of the fact and do parsing checks and use our add function
    if q_type == 'a':
        correct = ''
        while correct != 'a' and correct != 'b':
            correct = input("is this knowledge going to be true [A] or false [B]?: ").lower()

            if correct != 'a' and correct != 'b':
                print("please enter 'a' for true or 'b' for false.")
        
        if correct == "b":
            correct = False
        else:
            correct = True

        object, statement, subject = "", "", ""

        while object == '' and subject == '' and statement == '':
            new_knowledge = input("Please enter knowledge in the format: [subject is/was object]: ")
            doc = nlp(new_knowledge)
            for sen in doc.sentences:
                for word in sen.words:
                    if word.upos == "AUX":
                        statement = word.text.lower()
                    if word.upos == "PROPN":
                        subject = word.text.lower()
                    if word.upos == "NOUN":
                        object = word.text.lower()

            if object == '' and subject == '' and statement == '':
                print("not detecting noun or subject, please enter knowledge in the format; (SOMETHING is/was SOMETHING).")
        
        add_knowledge(statement, subject, object, correct)
        print(f"{subject} {statement} {object} is {correct} added to knowledge base")

    # if we are checking if something is true we parse the question and use the answer function
    if q_type == 'b':
        question = input("please ask a question about my knowledge base: ")
        doc = nlp(question)
        answer = answer_question(doc)
        print(answer)

    # if we the user chose to leave we save the knowledge base and exit the main loop
    if q_type == 'c':
        print("Goodbye.")

        with open("memory.dat", "wb") as f:
            pickle.dump(knowledge_base, f)

        done = True

