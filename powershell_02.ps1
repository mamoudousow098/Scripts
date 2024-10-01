# Initialize parameters
$classNames = @(
    "Connexion", "Fonction", "ResetPassword", "SalesmanUtilisateur", "Utilisateur", 
    "SessionUtilisateur", "Log", "Action", "Fonctionnalite", "LogAction", 
    "Module", "GroupeProxy", "JournalDeBord", "JournalDeBordEvenement", "Operation", 
    "OperationMois", "OperationSnsTrx", "Proxy", "SauvegardeSMS", "TemplateRepUssd", 
    "TemplateSMS", "TemplateUssd", "TotalNetworkGroup", "Transaction", "TransactionComplete", 
    "TransactionMois", "TransactionSansOperation", "TransactionSansOperationSauv", "USSDOperationMois", 
    "Agent", "AgentWH", "BizDev", "BizDevManager", "BizDevManagerGroup", "CategorieProduit", 
    "CategoryProxy", "CollectiviteLocale", "Commercial", "Compte", "Departement", 
    "Evt", "Grossiste", "GroupUser", "GroupeProxy", "KyaLevel", "ManagerSDGroup", 
    "Network", "NetworkGroup", "PDA", "Parametre", "ParametresCustomisationAgence", "PaysISO", 
    "Produit", "Proxy", "Region", "SalePoint", "SecteurActiviteAgence", "SponsorAgence", 
    "Status", "Statut", "SuperviseurGrossiste", "SuperviseurSD", "Supervisor", "Survey", 
    "TypeCompte", "TypeOperation", "USSDOperation", "USSDOperationComplete", "VisiteJournaliere", "Zone"
)

$directory = "C:\Users\MamoudouMamadouSOW\Documents\IntouchProjects\sansoperation"
$filePattern = "*.java"
$outputFile = "C:\Users\MamoudouMamadouSOW\Documents\tableNames.txt"

# Prepare the output file
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

# Regex for extracting @Table annotation
$tableRegex = '@Table\(name = "(.*?)"\)'

# Process each class name
foreach ($className in $classNames) {
    $filePath = Join-Path -Path $directory -ChildPath ("$className.java")

    # Check if the file exists
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw

        # Check for @Table annotation in the content
        if ($content -match $tableRegex) {
            # Extract all matches
            $matches = [regex]::Matches($content, $tableRegex)
            foreach ($match in $matches) {
                $tableName = $match.Groups[1].Value
                $result = "Class: $className, Table: $tableName, File: $filePath"
                Write-Output $result | Out-File -FilePath $outputFile -Append -Encoding UTF8
                Write-Output $result  # Also output to console
            }
        } else {
            $result = "No @Table annotation found in $filePath"
            Write-Output $result | Out-File -FilePath $outputFile -Append -Encoding UTF8
            Write-Output $result  # Also output to console
        }
    } else {
        $result = "No file found for $className at path $filePath"
        Write-Output $result | Out-File -FilePath $outputFile -Append -Encoding UTF8
        Write-Output $result  # Also output to console
    }
}
