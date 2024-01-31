# Zoom cloud meeting transcripts with OAuth

Transcribe your Zoom cloud recordings using AssemblyAI. Associated article - [How to get Zoom Transcripts with the Zoom API](https://www.assemblyai.com/blog/zoom-transcription-zoom-api/)

This script was tested using Python 3.10.5.

# Useful command to copy a repo and push it to your local 
git remote set-url origin http://github.com/YOU/YOUR_REPO  -- make sure the YOUR_REPO is created first

# Activate virtual environment
.venv/bin/activate

# Zoom recording Behaviour
The Zoom API's Behaviour is to call only the last recorded meeting. For all meetings a different approach has to be used. https://api.zoom.us/v2/past_meetings/{meetingId}/instances

* Follow up steps
* -- Challenges as most recordings are from personal rooms the meetings IDs are the same this makes it difficult to detect eaceh session. A new approach to schedule meetings is required
* -- Automate Download and append to table for all recordings on a given time by specific set of users. 
* -- Loop and pass transcription IDs to capture each dataframe and append a series of dataframes
