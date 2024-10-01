import re
from pathlib import Path

# Initialize parameters
# class_names = [
#     "Connexion", "Fonction", "ResetPassword", "SalesmanUtilisateur", "Utilisateur", 
#     "SessionUtilisateur", "Log", "Action", "Fonctionnalite", "LogAction", 
#     "Module", "GroupeProxy", "JournalDeBord", "JournalDeBordEvenement", "Operation", 
#     "OperationMois", "OperationSnsTrx", "Proxy", "SauvegardeSMS", "TemplateRepUssd", 
#     "TemplateSMS", "TemplateUssd", "TotalNetworkGroup", "Transaction", "TransactionComplete", 
#     "TransactionMois", "TransactionSansOperation", "TransactionSansOperationSauv", "USSDOperationMois", 
#     "Agent", "AgentWH", "BizDev", "BizDevManager", "BizDevManagerGroup", "CategorieProduit", 
#     "CategoryProxy", "CollectiviteLocale", "Commercial", "Compte", "Departement", 
#     "Evt", "Grossiste", "GroupUser", "GroupeProxy", "KyaLevel", "ManagerSDGroup", 
#     "Network", "NetworkGroup", "PDA", "Parametre", "ParametresCustomisationAgence", "PaysISO", 
#     "Produit", "Proxy", "Region", "SalePoint", "SecteurActiviteAgence", "SponsorAgence", 
#     "Status", "Statut", "SuperviseurGrossiste", "SuperviseurSD", "Supervisor", "Survey", 
#     "TypeCompte", "TypeOperation", "USSDOperation", "USSDOperationComplete", "VisiteJournaliere", "Zone"
# ]

class_names = [
    "Action",
    "Applicant",
    "Attachment",
    "TicketCategory",
    "Comment",
    "Control",
    "Environment",
    "Event",
    "Execution",
    "Form",
    "WorkflowGroup",
    "Input",
    "Internationalization",
    "LegalEntity",
    "TicketObjectType",
    "Ola",
    "TicketOrigin",
    "Parametre",
    "Persisted",
    "Problem",
    "Product",
    "Reference",
    "Sla",
    "Sop",
    "TicketStatus",
    "Step",
    "TicketTag",
    "Ticket",
    "TicketHistory",
    "TicketObject",
    "Treatment",
    "TicketType",
    "User",
    "UsersGroup",
    "Validator",
    "Workflow"
]
    

directory = Path(r"C:\Users\MamoudouMamadouSOW\Documents\IntouchProjects\GU2 - HT\ticketing-engine")
output_file = Path(r"C:\Users\MamoudouMamadouSOW\Documents\tableNames_ticketing.txt")

# Prepare the output file
if output_file.exists():
    output_file.unlink()

# Regex for extracting @Table annotation
#table_regex = re.compile(r'@Table\(name = "(.*?)"\)')
table_regex = re.compile(r'@Table\s*\(\s*name\s*=\s*"(.*?)"\s*\)')


# Process each class name
for class_name in class_names:
    # Search for files recursively
    for file_path in directory.rglob(f"{class_name}.java"):
        # Read the content of each file
        content = file_path.read_text()

        # Check for @Table annotation in the content
        matches = table_regex.findall(content)
        if matches:
            for table_name in matches:
                #result = f"Class: {class_name}, Table: {table_name}, File: {file_path}"
                result = f"{table_name}"
                with output_file.open('a', encoding='utf-8') as file:
                    file.write(result + "\n")
                print(result)
        else:
            pass
            # result = f"No @Table annotation found in {file_path}"
            # with output_file.open('a', encoding='utf-8') as file:
            #     file.write(result + "\n")
            # print(result)

# No need for a cleanup of a temp file since we're not creating any.
