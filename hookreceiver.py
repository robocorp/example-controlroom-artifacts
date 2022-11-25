from flask import Flask, request
import os
from RPA.HTTP import HTTP
from RPA.Robocorp.Process import Process


workspace_id = os.getenv("CONTROL_ROOM_WORKSPACE_ID")
workspace_api_key = os.getenv("CONTROL_ROOM_WORKSPACE_API_KEY")
process_id_filter = os.getenv("PROCESS_ID_FILTER", None)

if not workspace_id or not workspace_api_key:
    raise AttributeError(
        "Both environment variables 'CONTROL_ROOM_WORKSPACE_ID' and 'CONTROL_ROOM_WORKSPACE_API_KEY' need to be set for the server."
    )

flask_server = Flask(__name__)
CR = Process(
    workspace_id=workspace_id,
    workspace_api_key=workspace_api_key,
)


@flask_server.route("/", methods=["POST"])
def control_room_artifact_downloader():
    data = request.json
    process_id = data["payload"]["processId"]
    if process_id_filter and process_id_filter != process_id:
        print(f"Skipping events for process: {process_id}", flush=True)
        return data
    if data["event"] == "robot_run_event" and data["action"] == "END":
        process_run_id = data["payload"]["processRunId"]
        robot_run_id = data["payload"]["robotRunId"]
        artifacts = CR.list_run_artifacts(
            process_id=process_id,
            process_run_id=process_run_id,
            step_run_id=robot_run_id,
        )
        for artifact in artifacts:
            if artifact["fileName"].endswith(".png"):
                download_artifact(
                    artifact,
                    process_id,
                    process_run_id,
                    robot_run_id,
                )
            else:
                print(f'Skipping artifact: {artifact["fileName"]}', flush=True)
    else:
        print(f"Received event: {data['event']}", flush=True)
    return data


def download_artifact(
    artifact, process_id, process_run_id, robot_run_id, download=True
):
    artifact_download_url = CR.get_robot_run_artifact(
        process_run_id=process_run_id,
        step_run_id=robot_run_id,
        artifact_id=artifact["id"],
        process_id=process_id,
        filename=artifact["fileName"],
    )
    download_path = os.path.join(
        os.path.abspath("."), "results", f"artifact_{artifact['fileName']}"
    )
    print(f"\nArtifact download URL: {artifact_download_url}", flush=True)
    if download:
        HTTP().download(
            artifact_download_url,
            target_file=download_path,
        )
        print(f"\tDownloaded to: {download_path}", flush=True)


if __name__ == "__main__":
    flask_server.run(debug=True, port=8181)
