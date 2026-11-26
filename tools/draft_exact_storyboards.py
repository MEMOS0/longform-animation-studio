#!/usr/bin/env python3
"""Convert scene screenplays into continuous non-repeating exact-format director-seed storyboards.

These are not final director boards. They replace empty scaffold slots with the
scene's own images, decisions, dialogue, sound, and continuity objects so a
director/agent can revise precise staging shot by shot.
"""
import argparse,json,re
from pathlib import Path

deps=['mira_face_costume','child_face_scale_light','location_geography','relationship_continuity','sound_motif_continuity']
def minutes_range(v):
 m=re.search(r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)',v or '')
 return (float(m.group(1)),float(m.group(2))) if m else (0,5)
def build(scene):
 start,end=minutes_range(scene.get('time_range',''))
 duration=int(round((end-start)*60));count=10
 va=scene.get('visual_action',{});sound=scene.get('sound_design',{});dia=scene.get('dialogue_design',{})
 keys=(dia.get('key_lines') or ['']*2)+['','']
 beats=[
  ('wide establishing','slow push',va.get('first_image','opening image'),'none',sound.get('silence_or_negative_space','ambient negative space'),'hero','open on the scene image'),
  ('intimate closeup','settle',va.get('face_reaction','face reaction'),'none','breath and room tone','mid','read emotion before exposition'),
  ('action wide','lateral track',scene.get('objective','objective'),'none','environmental action foley','draft','objective as visible movement'),
  ('power two-shot','slow tightening',scene.get('conflict','conflict'),keys[0],sound.get('dialogue_priority','dialogue first'),'mid','conflict through voices and positions'),
  ('decision insert','macro',scene.get('protagonist_decision','protagonist decision'),'none','music drops before decision','mid','decision must be visible'),
  ('turn wide','reframe',scene.get('turn','scene turn'),'none','sound motif shifts','hero','power turn in space'),
  ('vertical composition','high or low angle',va.get('vertical_composition','power composition'),'none','negative space','draft','spatial power relationship'),
  ('subtext closeup','static intimate',scene.get('subtext','subtext'),keys[1],sound.get('music_function','sparse motif'),'mid','subtext not explanation'),
  ('consequence wide','backward track','consequence of '+scene.get('protagonist_decision','the decision'),'none','consequence foley','draft','cost becomes physical'),
  ('final image','slow pull-back',va.get('final_image','final image'),keys[0],sound.get('motif','motif')+' unresolved','hero','exit on changed power'),
 ]
 shots=[]
 for i in range(count):
  b=beats[round(i*(len(beats)-1)/max(1,count-1))]
  t=i*duration/count;e=(i+1)*duration/count
  shots.append({'shot_id':f"{scene['scene_id']}_DS{i+1:03d}",'timecode':f'{t:.1f}-{e:.1f}','duration_seconds':round(e-t,2),'scene_id':scene['scene_id'],'shot_size':b[0],'camera_intent':b[1],'visual_action':b[2],'dialogue':b[3],'sound_design':b[4],'generation_lane':b[5],'continuity_dependencies':deps,'director_note':'director seed generated from exact scene fields; refine staging before production: '+b[6]})
 return {'scene_id':scene['scene_id'],'duration_seconds':duration,'coverage':'continuous_exact_format_director_seed','shots':shots,'validation_rules':['seed must be manually/directorially refined before production','no gaps or overlaps','sound and power transitions must remain explicit']}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scenes',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 for p in sorted(Path(a.scenes).glob('S*.json')):
  obj=build(json.load(open(p,encoding='utf8')));q=out/(p.stem+'_director_seed.json');q.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(q)
if __name__=='__main__':main()
