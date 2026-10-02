"""Synthesise the 30 s soundtrack (numpy only, no external audio/API). Writes video/score.wav."""
import numpy as np, wave, sys
SR=44100; D=30.0; N=int(SR*D); BPM=120; B=60/BPM
r=np.random.default_rng(7); out=np.zeros((N,2))
def add(t,x,pan=0.0,g=1.0):
    i=int(t*SR); x=x[:max(0,N-i)]
    if i>=N or not len(x): return
    out[i:i+len(x),0]+=x*g*(1-max(0,pan)); out[i:i+len(x),1]+=x*g*(1+min(0,pan))
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def kick(): n=int(.35*SR);t=np.arange(n)/SR;f=45+120*np.exp(-t*28);return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.12)
def snare(): n=int(.25*SR);return (r.standard_normal(n)*.7+np.sin(2*np.pi*190*np.arange(n)/SR)*.5)*env(n,.001,.06)
def hat(o=False): n=int((.18 if o else .05)*SR);x=np.diff(r.standard_normal(n+1));return x*env(n,.001,.09 if o else .015)*.5
def bass(f,l): n=int(l*SR);t=np.arange(n)/SR;x=np.tanh(2.2*np.sin(2*np.pi*f*t)+.5*np.sin(4*np.pi*f*t));return x*env(n,.005,l*.8)*.6
def pad(f,l):
    n=int(l*SR);t=np.arange(n)/SR;x=sum(np.sin(2*np.pi*f*k*t+k)*(1/k) for k in(1,1.005,2,3))*.12
    return x*np.minimum(t/.5,1)*np.minimum((l-t)/.5,1)
def impact(): n=int(1.4*SR);t=np.arange(n)/SR;x=np.sin(2*np.pi*(40*np.exp(-t*3)+30)*t)*env(n,.002,.5)+r.standard_normal(n)*.35*env(n,.001,.25);return x*1.3
def riser(l): n=int(l*SR);t=np.arange(n)/SR;f=200+2600*(t/l)**2;x=np.sin(2*np.pi*np.cumsum(f)/SR)*.25+np.diff(r.standard_normal(n+1))*.25*(t/l);return x*(t/l)**2
def blip(f): n=int(.09*SR);t=np.arange(n)/SR;return np.sign(np.sin(2*np.pi*f*t))*env(n,.001,.05)*.18
roots=[55,55,65.4,49]  # A1 A1 C2 G1
beat=0
t=0.0
while t<D-.01:
    bar=int(t/(4*B)); b=int(round(t/B))%4; sec=t
    drive=sec>=3.0
    if sec<3.0:                      # hook: sparse heartbeat + tension
        if b in(0,2) and sec>1.0: add(t,kick(),g=.5)
        add(t,hat(),pan=.3,g=.4) if sec>1.5 else None
    else:
        if sec<25.5 or True:
            add(t,kick(),g=.95)
            add(t+B/2,hat(),pan=.4,g=.6); add(t+B/4,hat(),pan=-.4,g=.25); add(t+3*B/4,hat(),pan=-.4,g=.25)
            if b%2==1: add(t,snare(),g=.7)
            if b==3: add(t+B/2,hat(True),pan=-.3,g=.5)
            add(t+B/2,bass(roots[bar%4],B*.45),g=.8); add(t,bass(roots[bar%4],B*.45),g=.7)
            if sec>=6.5 and b==0: add(t,pad(roots[bar%4]*4,4*B),g=.7)
    t+=B
for rt,l in((1.0,2.0),(4.5,2.0),(10.5,2.0),(17.5,2.0),(23.5,2.0)): add(rt,riser(l),g=.55)
for it in(3.0,6.5,12.5,19.5,25.5): add(it,impact(),g=.9)
for it,f in((12.0,880),(16.4,660),(16.7,990),(24.2,1320)): add(it,blip(f),g=1)
for k,f in enumerate((523,659,784,1047)): add(26.7+k*.25,blip(f),g=1)
# final tail fade
fade=np.ones(N); fade[-int(1.2*SR):]=np.linspace(1,0,int(1.2*SR)); out*=fade[:,None]
out/=np.abs(out).max()*1.05; out=np.tanh(out*1.4)/np.tanh(1.4)
pcm=(out*32767*.9).astype('<i2')
with wave.open('score.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
print('ok',N/SR)
