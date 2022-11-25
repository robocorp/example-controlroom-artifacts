import os
from RPA.HTTP import HTTP
from RPA.Robocorp.Process import Process


workspace_id = os.getenv("CONTROL_ROOM_WORKSPACE_ID")
workspace_api_key = os.getenv("CONTROL_ROOM_WORKSPACE_API_KEY")

CR = Process(
    workspace_id=workspace_id,
    workspace_api_key=workspace_api_key,
)


def list_processes():
    processes = CR.list_processes()
    return processes


def list_process_runs(process):
    runs = CR.list_process_work_items(process_id=process["id"])
    runs = sorted(runs, key=lambda i: i["processRunNo"], reverse=True)
    return runs


def list_downloadable_artifacts(user_input, target_folder):
    artifacts = CR.list_run_artifacts(
        process_run_id=user_input["process_run_id"],
        step_run_id=user_input["activity_run_id"],
        process_id=user_input["process_id"],
    )
    downloads = []
    for artifact in artifacts:
        if user_input["filematch"] in artifact["fileName"]:
            download_link = CR.get_robot_run_artifact(
                process_run_id=user_input["process_run_id"],
                step_run_id=user_input["activity_run_id"],
                artifact_id=artifact["id"],
                filename=artifact["fileName"],
            )
            target_filepath = os.path.join(
                target_folder, f"{user_input['process_num']}_{artifact['fileName']}"
            )
            downloads.append(
                {
                    "filepath": target_filepath,
                    "link": download_link,
                    "filename": artifact["fileName"],
                }
            )

    return downloads


if __name__ == "__main__":
    processes = list_processes()
    for p in processes:
        print(p)
    print(processes[0].keys())
    runs = list_process_runs(processes[0])
    for r in runs:
        print(r["processRunNo"])
    print(runs)
    print(runs[0].keys())
