*** Settings ***
Library     RPA.Dialogs
Library     controlroom.py
Library     Collections
Library     RPA.HTTP


*** Tasks ***
Assistant for getting Control Room Artifacts
    ${processes}=    List Processes
    IF    len($processes)>1
        ${result}=    Request for process    ${processes}
        Set Task Variable    ${SELECTED_PROCESS}    ${result}
        ${finalresult}=    Request for process Run
    ELSE
        Set Task Variable    ${SELECTED_PROCESS}    ${processes}[0]
        ${finalresult}=    Request for process Run
    END
    ${downloads}=    List Downloadable Artifacts    ${finalresult}    ${CURDIR}${/}results
    IF    len($downloads) == 0
        Pass Execution    There are nothing to download
    END
    Add heading    Control Room Artifacts 3/3
    Add text    Download list:
    FOR    ${index}    ${down}    IN ENUMERATE    @{downloads}
        Add Text    ${downloads}[${index}][filename]
    END
    Run Dialog
    FOR    ${index}    ${down}    IN ENUMERATE    @{downloads}
        Download    url=${downloads}[${index}][link]
        ...    target_file=${downloads}[${index}][filepath]
        ...    overwrite=True
        ...    stream=True
    END


*** Keywords ***
Request for process
    [Arguments]    ${processes}
    Add heading    Control Room Artifacts 1/3
    ${namelist}=    Evaluate    [p['name'] for p in $processes]
    Add drop-down
    ...    name=selected_process
    ...    options=${namelist}
    ...    default=${namelist}[0]
    ...    label=Select a process
    ${result}=    Run dialog
    Log To Console    ${result}
    ${selected}=    Set Variable    ${result}[selected_process]
    ${process}=    Evaluate
    ...    list(filter(lambda process: process['name'] == '${selected}', $processes))
    RETURN    ${process}[0]

Request for process Run
    ${process_runs}=    List Process Runs    ${SELECTED_PROCESS}
    IF    len($process_runs) == 0
        Pass Execution    There are no process runs for a process: '${SELECTED_PROCESS}[name]'
    END
    ${namelist}=    Evaluate    [f"{r['processRunNo']} - {r['stateTs']}" for r in $process_runs]
    ${idlist}=    Evaluate    [r['id'] for r in $process_runs]
    ${names}=    Evaluate    ','.join($namelist)
    Add heading    Control Room Artifacts 2/3
    Add text    Process: ${SELECTED_PROCESS}[name]
    Add drop-down
    ...    name=selected_process_run
    ...    options=${names}
    ...    default=${namelist}[0]
    ...    label=Select a process run
    Add text input    filematch    label=Matching files
    ${result}=    Run dialog
    ${process_run}=    Evaluate    $result['selected_process_run'].split(" - ")[0]
    ${activity_id}=    Evaluate    list(filter(lambda run: run['processRunNo'] == ${process_run}, $process_runs))
    Set To Dictionary
    ...    ${result}
    ...    process_id=${activity_id}[0][processId]
    ...    process_run_id=${activity_id}[0][processRunId]
    ...    activity_run_id=${activity_id}[0][activityRunId]
    ...    workspace_id=${activity_id}[0][workspaceId]
    ...    process_num=${process_run}
    RETURN    ${result}
