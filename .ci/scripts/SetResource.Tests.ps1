# Pester tests for SetResource.ps1.
#
# Run with:
#   Install-Module Pester -Scope CurrentUser -Force
#   Invoke-Pester .ci/scripts/SetResource.Tests.ps1

BeforeAll {
    $script:ScriptPath = Join-Path $PSScriptRoot 'SetResource.ps1'

    # The Az cmdlets are not installed in CI, and these tests must not touch Azure.
    # Declare stubs so Pester has something to mock.
    function Get-AzResource {
        param($ResourceGroupName, $ResourceType, [switch]$ExpandProperties)
    }
    function Set-AzResource {
        param($ResourceId, $Tag, $ApiVersion, [switch]$Force)
    }
}

Describe 'UpdateLoop' {
    BeforeEach {
        # Returning no resources keeps the script's top-level tagging pass a no-op,
        # so dot-sourcing only imports the functions.
        Mock Get-AzResource { @() }
        Mock Start-Sleep { }

        . $script:ScriptPath -resourceGroupName 'rg' -tagId 'tag' -deploymentId 'dep'

        $script:resource = [pscustomobject]@{
            Id   = '/subscriptions/x/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/s'
            Tags = @{ tag = 'dep' }
            type = 'Microsoft.Storage/storageAccounts'
        }
    }

    It 'gives up after maxIterations when Set-AzResource keeps failing' {
        # Fail well past the retry budget, then start succeeding. A loop that does not
        # count its attempts therefore still terminates -- and fails on the assertions
        # below rather than hanging the test run forever.
        $script:attempts = 0
        Mock Set-AzResource {
            $script:attempts++
            if ($script:attempts -le 20) { throw 'persistent failure' }
        }

        { UpdateLoop -maxIterations 3 -resource $script:resource } |
            Should -Throw 'Failed to update resources'

        $script:attempts | Should -Be 3
    }

    It 'stops retrying as soon as Set-AzResource succeeds' {
        $script:attempts = 0
        Mock Set-AzResource {
            $script:attempts++
            if ($script:attempts -lt 2) { throw 'transient failure' }
        }

        { UpdateLoop -maxIterations 3 -resource $script:resource } | Should -Not -Throw

        $script:attempts | Should -Be 2
    }

    It 'does not retry when the first attempt succeeds' {
        Mock Set-AzResource { }

        { UpdateLoop -maxIterations 3 -resource $script:resource } | Should -Not -Throw

        Should -Invoke Set-AzResource -Times 1 -Exactly
    }
}
