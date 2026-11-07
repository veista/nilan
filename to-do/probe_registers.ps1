# Modbus TCP register probe (issue #3 matrix). Example: -ModbusHost 192.168.1.50
param(
    [string]$ModbusHost = "192.168.1.50",
    [int]$Port = 502,
    [int]$UnitId = 1
)

$ErrorActionPreference = "Stop"
$TransactionId = 1

$Registers = @(
    @{ Label = "filter_interval_inlet"; Type = "holding"; Address = 1326 },
    @{ Label = "filter_interval_exhaust"; Type = "holding"; Address = 1327 },
    @{ Label = "filter_remaining_inlet"; Type = "holding"; Address = 1328 },
    @{ Label = "filter_remaining_exhaust"; Type = "holding"; Address = 1329 },
    @{ Label = "filter_days_20103"; Type = "holding"; Address = 20103 },
    @{ Label = "room_setpoint_4746"; Type = "holding"; Address = 4746 },
    @{ Label = "room_setpoint_20102"; Type = "holding"; Address = 20102 },
    @{ Label = "fan_step_4747"; Type = "holding"; Address = 4747 },
    @{ Label = "fan_pct_21771"; Type = "holding"; Address = 21771 },
    @{ Label = "supply_fan_4699"; Type = "holding"; Address = 4699 },
    @{ Label = "extract_fan_4700"; Type = "holding"; Address = 4700 },
    @{ Label = "t4_20288"; Type = "holding"; Address = 20288 },
    @{ Label = "t5_20290"; Type = "holding"; Address = 20290 },
    @{ Label = "t6_20292"; Type = "holding"; Address = 20292 },
    @{ Label = "t8_20296"; Type = "holding"; Address = 20296 },
    @{ Label = "t4_5155"; Type = "holding"; Address = 5155 },
    @{ Label = "t5_5156"; Type = "holding"; Address = 5156 },
    @{ Label = "t6_5157"; Type = "holding"; Address = 5157 },
    @{ Label = "t8_5159"; Type = "input"; Address = 5159 },
    @{ Label = "dhw_setpoint_5548"; Type = "holding"; Address = 5548 },
    @{ Label = "dhw_setpoint_20460"; Type = "holding"; Address = 20460 },
    @{ Label = "dhw_top_5162"; Type = "input"; Address = 5162 },
    @{ Label = "humidity_4716"; Type = "input"; Address = 4716 },
    @{ Label = "avg_humidity_20164"; Type = "holding"; Address = 20164 },
    @{ Label = "op_mode_5432"; Type = "holding"; Address = 5432 }
)

function Read-ModbusRegister {
    param(
        [System.Net.Sockets.TcpClient]$Client,
        [string]$Type,
        [int]$Address,
        [byte]$Unit
    )

    $functionCode = if ($Type -eq "input") { 0x04 } else { 0x03 }
    $tid = [byte[]]([bitconverter]::GetBytes([uint16]$script:TransactionId))
    if ([BitConverter]::IsLittleEndian) { [array]::Reverse($tid) }
    $script:TransactionId++

    $pdu = [byte[]]@(
        $Unit,
        $functionCode,
        [byte](($Address -shr 8) -band 0xFF),
        [byte]($Address -band 0xFF),
        0x00,
        0x01
    )
    $length = [byte[]]([bitconverter]::GetBytes([uint16]($pdu.Length)))
    if ([BitConverter]::IsLittleEndian) { [array]::Reverse($length) }
    $frame = $tid + @(0x00, 0x00) + $length + $pdu

    $stream = $Client.GetStream()
    $stream.Write($frame, 0, $frame.Length)

    Start-Sleep -Milliseconds 150

    $buffer = New-Object byte[] 256
    $read = 0
    $deadline = (Get-Date).AddSeconds(3)
    while ($read -lt 9 -and (Get-Date) -lt $deadline) {
        if ($stream.DataAvailable) {
            $chunk = $stream.Read($buffer, $read, $buffer.Length - $read)
            if ($chunk -le 0) { break }
            $read += $chunk
        } else {
            Start-Sleep -Milliseconds 20
        }
    }

    if ($read -lt 9) {
        return @{ Status = "error"; Detail = "timeout" }
    }

    $respUnit = $buffer[6]
    $respFc = $buffer[7]
    if ($respFc -band 0x80) {
        $exc = $buffer[8]
        return @{ Status = "exception"; ExceptionCode = $exc }
    }

    $byteCount = $buffer[8]
    if ($byteCount -lt 2) {
        return @{ Status = "error"; Detail = "short response" }
    }

    $value = ($buffer[9] -shl 8) + $buffer[10]
    return @{ Status = "ok"; Value = $value }
}

$client = New-Object System.Net.Sockets.TcpClient
$client.ReceiveTimeout = 3000
$client.SendTimeout = 3000
$client.Connect($ModbusHost, $Port)

$rows = @()
foreach ($reg in $Registers) {
    $outcome = Read-ModbusRegister -Client $client -Type $reg.Type -Address $reg.Address -Unit $UnitId
    $row = [ordered]@{
        label   = $reg.Label
        type    = $reg.Type
        address = $reg.Address
        status  = $outcome.Status
    }
    if ($outcome.ContainsKey("Value")) { $row.value = $outcome.Value }
    if ($outcome.ContainsKey("ExceptionCode")) { $row.exception_code = $outcome.ExceptionCode }
    if ($outcome.ContainsKey("Detail")) { $row.detail = $outcome.Detail }
    $rows += [pscustomobject]$row
}

$client.Close()

$alive = @($rows | Where-Object { $_.status -eq "ok" })
$dead = @($rows | Where-Object { $_.status -ne "ok" })

Write-Output "PROBED_AT=$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
Write-Output "HOST=$ModbusHost`:$Port UNIT=$UnitId ALIVE=$($alive.Count) DEAD=$($dead.Count)"
$rows | Format-Table -AutoSize | Out-String -Width 200 | Write-Output

$matrixPath = Join-Path $PSScriptRoot "register-probe-matrix.md"
$md = @"
# CTS700 register probe matrix

Probed: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')  
Host: $ModbusHost`:$Port · Unit ID: $UnitId

| Label | Type | Address | Status | Value / code |
|-------|------|---------|--------|--------------|
"@
foreach ($r in $rows) {
    $val = if ($r.status -eq "ok") { $r.value } elseif ($r.exception_code) { "exception $($r.exception_code)" } else { $r.detail }
    $md += "| $($r.label) | $($r.type) | $($r.address) | $($r.status) | $val |`n"
}
$md += @"

## Summary

- Alive: $($alive.Count)
- Dead/exception: $($dead.Count)

## Recommended fallbacks (issue #3 / PR #4)

"@
if (($rows | Where-Object { $_.label -eq "filter_days_20103" -and $_.status -ne "ok" })) {
    $md += "- Filter days: use **1328/1329** (remaining) and **1326/1327** (interval); days-since = interval - remaining`n"
}
if (($rows | Where-Object { $_.label -eq "fan_pct_21771" -and $_.status -ne "ok" })) {
    $md += "- Fan percent: use **4699/4700** instead of 21771`n"
}
if (($rows | Where-Object { $_.label -eq "dhw_setpoint_20460" -and $_.status -ne "ok" })) {
    $md += "- DHW setpoint: use **5548** instead of 20460`n"
}
if (($rows | Where-Object { $_.label -match "^t[456]_202" -and $_.status -ne "ok" })) {
    $md += "- T4-T6: use **5155-5157** instead of 20288-20292`n"
}
Set-Content -Path $matrixPath -Value $md -Encoding UTF8
Write-Output "WROTE=$matrixPath"
