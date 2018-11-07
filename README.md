## Introduction
A speech to text front-end AGI script for an Asterisk server. 
Includes a dialplan example to show how to interface the script
as an AGI or EAGI

#### Build environment: 
- Debian GNU/Linux 9 (stretch) 
- Asterisk.v13-LTS-certified.
- Python2.7

## Installation
Run the installer (for centos6)
```bash
$ sh installer.sh
```
(Installation scripts will be added for other OS on request basis)

## Guide
```bash
# /etc/asterisk/extensions.conf
[context]
exten => extension,1,Answer()
	same => n,Set(SessionId="") 
	same => n,Set(ReadDtmf="")
	same => n,Set(Terminate="")
	same => n,Set(CallAgent="")
	same => n,Set(ClientId="client-id")
	same => n,Set(AccessToken="TOKEN")
	same => n,Set(VirtualNumber="number")
	same => n,Set(HostUrl="")
	same => n,Goto(context,speechToTextExtension,1)
	
	# ... continued below
```

1. Route the call to any extension answer the call to avoid hangups.
2. Set an empty `SessionId` the script will automatically add a uuid(v4) SessionId.
3. `ReadDtmf`: A flag to set if DTMF has to be read.
4. `Terminate`: A flag to set if the call should be terminated.
5. `CallAgent`: A flag to set if the call should be transferred to an agent.
6. Set the integration settings as provided.
7. Once the configurations are complete, route to another extension.

```bash
# /etc/asterisk/extension.conf
exten => speechToTextExtension,1,NoOp(${HostUrl},${SessionId},${ClientId},${AccessToken},${VirtualNumber})
	same=> n(listen),eagi(listen_and_speak.py,${HostUrl},${SessionId},${ClientId},${AccessToken},${VirtualNumber})
	same => n,NoOp(${PlayFile}, ${SessionId}, ${Terminate}, ${CallAgent})
	same => n(onmessage),GotoIf($[${EXISTS("${PlayFile}")}]?checklen:listen)
	same => n(checklen),GotoIf($["${PlayFile}" != ""]?prompt:listen)
	same => n(prompt),Playback(${PlayFile}, skip)	
	same => n,GotoIf($[${Terminate} != ""]?hangup)
	same => n,NoOp(${CallAgent})

    # ==============================
    # replace context,extension,priority
    # with the logic to connect to
    # any available agent
	same => n,GotoIf($["${CallAgent}" != ""]?context,extension,priority)

	same => n,Playback(beep, skip) # Can be omitted
	same => n,Set(PlayFile="")
	same => n,NoOp(${PlayFile}, ${ReadDtmf})
	same => n,GotoIf($[${EXISTS("${ReadDtmf}")}]?checkdtmf:listen)
	same => n(checkdtmf),GotoIf($["${ReadDtmf}" != ""])?readdtmf:listen)
	same => n(readdtmf),Read(DtmfVal)
	same => n,NoOp(${DtmfVal})
	same => n,agi(sendDTMFMessage.py,${HostUrl},${SessionId},${ClientId},${AccessToken},${VirtualNumber},${DtmfVal})
	same => n,Set(DtmfVal="")
	same => n,Set(ReadDtmf="")
	same => n,Goto(onmessage)
	same => n,Set(SessionId="")
	same => n(hangup),Hangup()
```
1. `listen_and_speak.py` listens for sound on channel 3
and sends .FLAC files to the configured `HostUrl` make sure to save 
the sound files to be played as response to the sound.
2. Ensure the sound files are `.mp3` (currently this is the only format supported). 
3. `PlayFile`: A flag to be set with the name of the file to be played.
4. `DtmfVal`: Set this with the DTMF read.
5. `sendDTMFMessage.py`: sends DTMF tones to the configured `HostUrl` service.
6. This dialplan listens indefinitely for sound inputs.
