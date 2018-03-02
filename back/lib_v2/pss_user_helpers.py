def generate_username(user_dict):            
    return "%s%s"%(user_dict['first_name'].lower(),user_dict['last_name'].lower())
        
