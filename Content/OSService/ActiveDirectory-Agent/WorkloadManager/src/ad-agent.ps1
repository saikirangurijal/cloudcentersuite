try {
    Start-Transcript -Path C:\temp\Join-Domain.log -Append
    $envPath = 'C:\temp\userenv.ps1'
    . $envPath 

    $domainEnv = Get-ChildItem Env:domain
    $userNameEnv = Get-ChildItem Env:userName
    $dnsServerIpEnv = Get-ChildItem Env:dnsServerIp
    $passwordEnv = Get-ChildItem Env:domainPassword

    $wmi = Get-WmiObject win32_networkadapterconfiguration
    $wmi.SetDNSServerSearchOrder($dnsServerIpEnv.value) 

    $pass = ConvertTo-SecureString $passwordEnv.value -AsPlainText -Force
    $fullUserName = $domainEnv.value + "\" + $userNameEnv.value
    $cred = New-Object System.Management.Automation.PSCredential ($fullUserName,$pass)
    Add-Computer -DomainName $domainEnv.value -Credential $cred -Restart -Force
}
catch {
    $error[0]|format-list -force  #print more detail reason for failure   
}