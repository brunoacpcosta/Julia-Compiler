import re

class PrePro:

    @staticmethod
    def filter(string):
        pattern = "(#=)(.*?)(=#)"
        replace = ""
        filtered = re.sub(pattern, replace, string) 
        return filtered

