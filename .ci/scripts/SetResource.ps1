param (
    [string] $resourceGroupName,
    [string] $tagId, 
    [string] $deploymentId
)

$projectTags = New-Object 'System.Collections.Generic.Dictionary[String,String]'
$projectTags.Add($tagId, $deploymentId)

function UpdateLoop
{
    param( [int]$maxIterations, $resource )

    $success = $false
    $iterator = 1

    while( ($success -eq $false) -and ($iterator -le $maxIterations))
    {
        try 
        {
            if($resource.type -eq "Microsoft.MachineLearningServices/workspaces")
            {
                Set-AzResource -ResourceId $resource.Id -Tag $resource.Tags -ApiVersion 2019-06-01 -Force
            }
            else
            {
                Set-AzResource -ResourceId $resource.Id -Tag $resource.Tags -Force
            }

            $success = $true
            break
        }
        catch 
        {
            Write-Host("Failed to write resource update - ")
            Write-Host($_.Exception.Message)
            Start-Sleep -Seconds 5
        }
    }

    if($success -eq $false)
    {
        throw "Failed to update resources"
    }
}


function Update-GroupResources 
{
    param( [string]$resGroup, $tags )
    Write-Host("*************** Updating resources in " + $resGroup)
    $resources = Get-AzResource -ResourceGroupName $resGroup 
    $resources | ForEach-Object {
        if($_.Tags -eq $null)
        {
            $_.Tags = $projectTags
        }
        else {
            $rsrc = $_
            $tags.Keys | Foreach {
                $rsrc.Tags[$_] = $tags[$_] 
            }
        }
    }
    $resources | ForEach-Object {
        Write-Host("*************** Updating resource " + $_.Id)
        UpdateLoop -maxIterations 3 -resource $_
    }
}


Write-Host("RG - " + $resourceGroupName)
Write-Host("TAG - " + $tagId)
Write-Host("VAL - " + $deploymentId)

Update-GroupResources -resGroup $resourceGroupName -tags $projectTags

$clusterResources = Get-AzResource -ResourceType "Microsoft.ContainerService/managedClusters" -ResourceGroupName $resourceGroupName -ExpandProperties
foreach($cluster in $clusterResources)
{
    Update-GroupResources -resGroup $cluster.Properties.nodeResourceGroup -tags $projectTags
}
