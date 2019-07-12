# Add Computer to domain
# Author : Riyas Ahamed

try {
    # Server logs
    Start-Transcript -Path C:\temp\Join-Domain.log -Append

    # Load environment variables
    $envPath = 'C:\temp\userenv.ps1'
    . $envPath 

    $domainEnv = Get-ChildItem Env:domain -ErrorAction Stop;
    $userNameEnv = Get-ChildItem Env:userName -ErrorAction Stop;
    $dnsServerIpEnv = Get-ChildItem Env:dnsServerIp -ErrorAction Stop;
    $passwordEnv = Get-ChildItem Env:domainPassword -ErrorAction Stop;

    # Set domain IP to Network Adapter
    $wmi = Get-WmiObject win32_networkadapterconfiguration -ErrorAction Stop;
    $wmi.SetDNSServerSearchOrder($dnsServerIpEnv.value) 

    # Convert Plain Text Password to Secure String Password
    $pass = ConvertTo-SecureString $passwordEnv.value -AsPlainText -Force -ErrorAction Stop;
    $fullUserName = $domainEnv.value + "\" + $userNameEnv.value

    # Create Credential Object
    $cred = New-Object System.Management.Automation.PSCredential ($fullUserName,$pass) -ErrorAction Stop;

    # Add Local Computer to Domain with Credential
    Add-Computer -DomainName $domainEnv.value -Credential $cred -ErrorAction Stop;
}
catch {
    # Catch Exception 
    Write-Host "CLIQR_EXTERNAL_SERVICE_ERR_MSG_START"
    $_.Exception.Message  #print more detail reason for failure   
    Write-Host "CLIQR_EXTERNAL_SERVICE_ERR_MSG_END"
    exit 127;
}