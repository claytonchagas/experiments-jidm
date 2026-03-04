$foldersList = "folders.txt"
$argumentsFile = "arguments.txt"
$currentDir = Get-Location

if (!(Test-Path $foldersList)) {
    Write-Host "Erro: Arquivo $foldersList não encontrado em $currentDir" -ForegroundColor Red
    return
}

$globalArgs = ""
if (Test-Path $argumentsFile) {
    $globalArgs = (Get-Content $argumentsFile) -join " "
}

$targetFolders = Get-Content $foldersList

foreach ($folderRelativePath in $targetFolders) {
    $folderPath = Join-Path $currentDir $folderRelativePath.Trim()

    if (Test-Path $folderPath) {
        Write-Host "`n--- Acessando: $folderRelativePath ---" -ForegroundColor Blue
        
        $dataflowDir = Join-Path $folderPath "dataflows"
        if (!(Test-Path $dataflowDir)) { 
            New-Item -ItemType Directory -Path $dataflowDir | Out-Null 
        }

        $pyFiles = Get-ChildItem -Path $folderPath -Filter "*modular*.py"

        foreach ($file in $pyFiles) {
            $name = $file.BaseName
            Write-Host "  > Processando proveniência: $($file.Name)" -ForegroundColor Cyan

            Push-Location $folderPath

            # Check for a local arguments.txt inside the folder, else use global
            $localArgsFile = Join-Path $folderPath "arguments.txt"
            $runArgs = if (Test-Path $localArgsFile) {
                (Get-Content $localArgsFile) -join " "
            } else {
                $globalArgs
            }

            try {
                if ($runArgs -ne "") {
                    now run "$($file.Name)" $runArgs.Split(" ")
                } else {
                    now run "$($file.Name)"
                }

                # Get the most recent trial ID from now list
                $listOutput = now list 2>$null
                $trialId = $null
                foreach ($line in $listOutput) {
                    if ($line -match '\[.\]Trial\s+([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})') {
                        $trialId = $Matches[1]
                    }
                }

                if (-not $trialId) {
                    Write-Warning "  Nenhum trial encontrado para $($file.Name), pulando exportação."
                } else {
                    Write-Host "  Trial: $trialId" -ForegroundColor DarkCyan

                    $dotFile = Join-Path $dataflowDir "$name.dot"
                    $svgFile = Join-Path $dataflowDir "$name.svg"

                    $dotContent = now dataflow $trialId -d 1 2>$null
                    [System.IO.File]::WriteAllLines($dotFile, $dotContent)

                    $firstLine = Get-Content "$dotFile" -TotalCount 1 -ErrorAction SilentlyContinue
                    if ($firstLine -notmatch "^digraph|^strict") {
                        Write-Warning "  Exportação inválida para $($file.Name): $firstLine"
                        Remove-Item "$dotFile" -Force -ErrorAction SilentlyContinue
                    } else {
                        Write-Host "  [OK] $name.dot gerado." -ForegroundColor Green
                        if (Get-Command "dot" -ErrorAction SilentlyContinue) {
                            dot -Tsvg "$dotFile" -o "$svgFile"
                        }
                    }
                }
            }
            finally {
                Pop-Location
            }
        }
    } else {
        Write-Warning "Pasta não encontrada: $folderRelativePath"
    }
}

Write-Host "`nAutomação concluída!" -ForegroundColor Yellow