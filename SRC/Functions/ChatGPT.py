import Log
import openai

class ChatGPT:

    # Function to configure the help function and prepare it for use
    def __init__(self):
        self.Argument = None
        self.Communicate = None
        self.commandsFile = None
        self.AdditionalArgs = None
        self.NameModule = "/gpt"
        self.Dependency_Dict = {
            'Whisper': None
        }

        self.log = Log.Generate()

        try:
            openai.api_key = "SET YOUR API KEY HERE"
        except Exception as error:
            self.log.Write("ChatGPT.py | OpenAI # " + str(error))

    def requirements(self):

        requeriments = {
            # In CommandExecution is necessary define the name that the user will use to call the command
            'CommandExecution': "/gpt",
            # In ExternalModules is necessary define the modules necessary to make the module work in the list
            # >> commandsFile: is a dictionary with the commands and the information of the command
            # >> Communicate: is an object that will be used to communicate with the user
            # >> InterfaceController: is an object that will be used to control the web WhatsApp interface
            # >> Schedule: is an object that will be used to control the schedule of the module
            'ExternalModules': [
                'commandsFile', 'Communicate'
            ],
            # In Dependencies is necessary define the modules necessary to make the module work in the list
            # >> Whisper: is a module that transform the speech to text
            'Dependencies': {
                'Whisper': '0.2.0'
            }
        }

        return requeriments

    def set_Communicate(self, Communicate):
        self.Communicate = Communicate

    def set_commandFile(self, commandsFile):
        self.commandsFile = commandsFile

    def set_dependency(self, dependency_name, Module):
        try:
            self.Dependency_Dict[dependency_name] = Module
            print("Test")
        except Exception as error:
            self.log.Write("ChatGPT.py | Error of Dependency # " + str(error))


    def __PrepareArgs(self, args, additionalArgs):
        if args in self.commandsFile['Active'][self.NameModule]['Args'][0].keys():
            self.Argument = args

            if additionalArgs is not None:
                self.AdditionalArgs = additionalArgs

            return True
        else:
            return False

    # This function is used to initialize the help function
    def EntryPoint(self, args=None, additionalArgs=None):

        # if args is empty or None execute default function else execute different function depending on the args
        if args is None:
            return self.Default()
        else:
            # check if args exist and is a valid argument
            if self.__PrepareArgs(args, additionalArgs):
                # Execute the function in charge of managing the help function
                    return self.CommandManager()
            else:
                return False

    # This function is used to function to management of the help functions and execute the correct function
    def CommandManager(self):

        if self.Argument == '-d':
            return self.DescribeCommand()
        elif self.Argument == '-l':
            return self.ListArgs()
        elif self.Argument == '-s':
            return self.Speech()
        elif self.Argument == '-t':
            return self.Text()
        else:
            return False

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    def DescribeCommand(self):
        return self.commandsFile['Active'][self.NameModule]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active'][self.NameModule]['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    def Speech(self):

        try:

            # Get the speech from the user
            Speech = self.Dependency_Dict['Whisper'].init_function("Transcribe")

            # Send the speech to the GPT-3 API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                #delete the first character of the speech
                messages=[
                    {'role': 'user', 'content': Speech[1][3:]}
                ],
                max_tokens=100,
            )

            # Send the response to the user
            self.Communicate.WriteMessage(response['choices'][0]['message']['content'])
            self.Communicate.SendMessage()

            return ['', 'ChatGPT Finished']

        except Exception as error:
            self.log.Write("ChatGPT.py | Speech # " + str(error))
            return ['', 'ChatGPT Error']
    def Text(self):
        pass