import configparser
import os 
import sys 
import re 

import streamlit as st
from dateutil.parser import ParserError
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from dateutil.parser import parse
from datetime import timedelta
from ai_models.deid.static_pattern_builder import static_patterns
from ai_models.deid.date_utils import DateUtils
class Deidentification:
    def __init__(self):
        config = configparser.ConfigParser()
        if hasattr(sys, '_MEIPASS'):
            pp = os.path.join(sys._MEIPASS, "model_config/model-config.conf")
        else:
            pp = "model_config/model-config.conf"
        fp = open(pp)
        config.read_file(fp)
        self.date_shift_factor = int(config.get('deid-config', 'date_shift_factor'))
        if hasattr(sys, '_MEIPASS') and getattr(sys, 'frozen', False):
            path_prefix = os.path.dirname(sys.executable)
            self.deid_model_path = os.path.join(path_prefix, config.get('deid-config', 'deid_model'))
        else:
            self.deid_model_path = config.get('deid-config', 'deid_model')
        self.ner_pip = self.initialize_model()
        self.static_patterns = static_patterns
        self.REGEX_SPLIT_CHAR = "\\|"
        self.STRING_SPLIT_LINES = "\\n\\r?"
        self.STRING_SPLIT_WORDS = "\\n"
        self.DIGIT = "\\d"
        self.UPPERCASE_LETTER = "[A-Z]"
        self.LOWERCASE_LETTER = "[a-z]"
        self.candidate_pii_strs = ['00-A-APP|BP 111/11|A111AA1AA1234567','jpocsap01','01-L-APP-PACS_Admins_advanced']
        self.update_static_patterns()
        self.ignore_texts = ["vue",'vuemotion','pacs','happy','ldap','app','MIRTH','Philips','will','don','hi','hyperv','Hey,hyper-v','Hello','weeks','mammo','precision','carestream','fuse','rad','RAD','v-motions','fetch','best','medicom','light','hope','max','explorer','tomo','epic','chance','archive','hospital','NIC','eis','logins','computing','wfm','FOLLOWING MAMMO','Shaking','drafts','Explorer','microsoftedge','vuepacs','windows10','Vue' ,'products','cerner','mcafee','dha','Slice','him','black','stills','quick','night','mock','vhcpacs','carestreampacs','Vue-Explorer','windows11','mediprime','min','info','vue motion','Bonjour','EDI','powershare','Philips EDI','quick','json','fiddler','customer','loader','exe','oracle','isilon','fir','csa','lda','logon','CONN','eis','mammo','philips','windows','_' ]
        self.ignore_texts = [x.lower() for x in self.ignore_texts]

        fp.close()
        self.date_util_ob = DateUtils()
    def update_static_patterns(self):
        candidate_pii_regex_dict_list = self.generate_regexp_from_pattern()   
        for candidate_pii_regex_dict in candidate_pii_regex_dict_list:
            self.static_patterns.update(candidate_pii_regex_dict) 
    
    def initialize_model(self):
        model = AutoModelForTokenClassification.from_pretrained("C:\\Anshul\\deid\\DeId-project\\DeId-project\\serviceability-ai-enablers\\ai-enablers\\model_files\\deid\\stanford-deidentifier-base")
        tokenizer = AutoTokenizer.from_pretrained("C:\\Anshul\\deid\\DeId-project\\DeId-project\\serviceability-ai-enablers\\ai-enablers\\model_files\\deid\\stanford-deidentifier-base")
        pip = pipeline("ner", model=model, tokenizer=tokenizer)
        return pip
    
    def generate_regexp_from_pattern(self):
        created_regex_list = []
        for pattern_idx ,  pattern in enumerate(self.candidate_pii_strs):
            cand_regex = ""
            for c in pattern:
                if c.isdigit():
                    cand_regex += self.DIGIT
                elif c.isalpha() and c.isupper():
                    cand_regex += self.UPPERCASE_LETTER
                elif c.isalpha() and c.islower():
                    cand_regex += self.LOWERCASE_LETTER
                else:
                    cand_regex +=  c
            created_regex_list.append({"created_regex"+str(pattern_idx):cand_regex})
        return created_regex_list

                



    def analyse_rules(self,text):
        phi_info = []
        for pattern in self.static_patterns:
            matches = re.finditer(self.static_patterns[pattern], text)
            if any(matches) :
                for m in matches:
                    
                    phi_info.append({"startIndex":m.start(),
                    "endIndex": m.end(),
                    "phiText":text[m.start():m.end()]})
        return phi_info

            
        
        
    def shift_date(self,phi_info):
        for i , phi in enumerate(phi_info):
            
            flag , date = self.date_util_ob.is_valid_date(phi["phiText"])
            if flag:
                original_date = date
                print("dt**",original_date)
                shifted_date = original_date + timedelta(days=365 * self.date_shift_factor)
                result_date_string = shifted_date.strftime(original_date.strftime("%Y-%m-%d"))
                phi_info[i]["phiText"] = result_date_string
        return phi_info

            
    
    def merge_text(self,results):
        print(results)
        for i in range(len(results) - 1):
            if (results[i + 1]['start'] == results[i]['end']) or (results[i]['end'] > results[i + 1]['start']) or (
                    results[i + 1]['start'] == results[i]['end'] + 1):
                results[i + 1]['start'] = results[i]['start']
                results[i + 1]['word'] = results[i]['word'].replace('#', '') + results[i + 1]['word'].replace('#', '')
                results[i] = None
        return results

    def hash_phi(self , phi_info , input_str ):
        for i , phi in enumerate(phi_info):
            start_index = phi["startIndex"]
            end_index = phi["endIndex"]
            phi_text = input_str[start_index:end_index+1]
            date_flag , _ = self.date_util_ob.is_valid_date(phi_text)
            if date_flag: 
                continue
            else:
                    input_str = input_str[:start_index] + '#' * (end_index - start_index + 1) + input_str[end_index + 1:]
        return input_str
            
    def get_deidentified_text(self,text):
        try:
            results = self.ner_pip(text)
            results = self.merge_text(results)
        except Exception as e:
            results = []
        
        phi_info = []
        for i in range(len(results)):
            if results[i] is not None:
                results_out = {}
                results_out['startIndex'] = results[i]['start']
                results_out['endIndex'] = results[i]['end']
                results_out['phiText'] = results[i]['word']
                results_out['entity'] = results[i]['entity']
                phi_info.append(results_out)
        rule_engine_outputs = self.analyse_rules(text)
    
        phi_info.extend(rule_engine_outputs)
        phi_info = self.shift_date(phi_info)
        phi_removed_text = self.hash_phi(phi_info , text )
        return phi_removed_text
    
if __name__=="__main__":
        ## streamlit app
    # st.set_page_config(page_title="Can you please de-identify text")
    # st.header("Gemini App to extract PHI")

    # question=st.text_input("Input:", key="input")
    # submit= st.button("Ask the question")

    deid = Deidentification()
    response=deid.get_deidentified_text(text="PROCEDURE: Chest xray. COMPARISON: last seen on 1/1/2020 and also record \n dated of March 1st, 2019. FINDINGS: patchy airspace opacities. IMPRESSION: \n The results of the chest xray of January 1 2020 are the most concerning \n ones. The patient was transmitted to another service of UH Medical Center \n under the responsability of Dr. Perez. We used the system MedClinical data \n transmitter and sent the data on 2/1/2020, under the ID 5874233. We \n received the confirmation of Dr Perez. He is reachable at 567-493-1234. \n - text: Dr. Curt Langlotz chose to schedule a meeting on 06/23.")
    print(response)
    # if submit:
    #     response=deid.get_deidentified_text(question=question)
    #     print(response)
    #     st.subheader("The response is")
    #     st.header(response)
