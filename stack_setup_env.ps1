Clear-Host

$pyENV = Read-Host -Prompt "Enter name of Python environment for QED: "
[Environment]::SetEnvironmentVariable("QED_PY_ENV",$pyENV, "User")
Write-Host "Setting QED_PY_ENV = $pyENV"

$flaskPath = Read-Host -Prompt "Enter the path to the flask_qed directory for celery: "
[Environment]::SetEnvironmentVariable("QED_FLASK_PATH",$flaskPath, "User")
Write-Host "Setting QED_FLASK_PATH = $flaskPath"

$redisPath = Get-ChildItem "C:\Program Files\Redis" -Filter redis-server.exe -Recurse -ErrorAction SilentlyContinue | % {$_.FullName}
If ($redisPath -eq ""){
	Write-Host "Unable to find an installation of Redis. Please install redis."
}
Else {
	[Environment]::SetEnvironmentVariable("REDIS_PATH",$redisPath, "User")
	Write-Host "Setting REDIS_PATH = $redisPath"
}

$mongodbPath = Get-ChildItem "C:\Program Files\MongoDB" -Filter mongod.exe -Recurse -ErrorAction SilentlyContinue | % {$_.FullName}
If ($mongodbPath -eq ""){
	Write-Host "Unable to find an installation of MongoDB. Please install mongoDB."
}
Else{
	[Environment]::SetEnvironmentVariable("MONGODB_PATH",$mongodbPath, "User")
	Write-Host "Setting MONGODB_PATH = $mongoDB"
}

Read-Host "Press enter to exit..."