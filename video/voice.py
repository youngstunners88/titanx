"""Local voice-over (Piper neural TTS, runs offline, no API/credits). Writes video/voice.wav aligned to the scene timeline.
Model: en_US-ryan-high from rhasspy/piper-voices (free download). Usage: PYTHONPATH=/tmp/pylibs python3 voice.py"""
import wave, io, subprocess, numpy as np, sys
from piper import PiperVoice
FF='/tmp/pylibs/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
SR=44100
# (start s, max seconds, line)   -- starts match the visual beats in scene.template.html
LINES=[(.25,1.5,"Your project is brilliant."),(1.75,1.2,"Nobody saw it."),
 (3.3,1.1,"I'm Young Stunners."),(4.5,1.95,"I make short videos. Real campaigns."),
 (6.9,2.0,"You send the brief."),(9.05,2.9,"I write it. Shoot it. Cut it."),(12.0,.9,"You approve."),
 (12.75,3.3,"Then I push it across X and Instagram."),(16.35,3.0,"Thirty-eight projects. A hundred and thirty posts."),
 (19.7,3.6,"Promo videos and campaigns for Web3 teams."),(24.0,1.9,"Latest drop: Lil Blunt."),
 (26.0,3.4,"Book a campaign. Young Stunners.")]
v=PiperVoice.load('/tmp/voices/en_US-ryan-high.onnx')
N=int(SR*30); out=np.zeros(N)
for st,mx,txt in LINES:
    b=io.BytesIO()
    with wave.open(b,'wb') as w: v.synthesize_wav(txt,w)
    b.seek(0); open('/tmp/_l.wav','wb').write(b.read())
    def load(tempo):
        p=subprocess.run([FF,'-loglevel','error','-i','/tmp/_l.wav','-af',f'atempo={tempo},silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse','-ar',str(SR),'-ac','1','-f','s16le','-'],capture_output=True).stdout
        return np.frombuffer(p,dtype='<i2')/32768
    x=load(1.0); d=len(x)/SR; t=1.0
    if d>mx: t=min(1.35,d/mx); x=load(round(t,3))
    i=int(st*SR); x=x[:N-i]; fade=int(.02*SR); x[:fade]*=np.linspace(0,1,fade); x[-fade:]*=np.linspace(1,0,fade)
    out[i:i+len(x)]+=x
    print(f'{st:5.2f}s {len(x)/SR:4.2f}s/{mx} tempo {t:.2f}  {txt}',file=sys.stderr)
out=np.tanh(out/np.abs(out).max()*1.6)/np.tanh(1.6)*.95
with wave.open('voice.wav','wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
