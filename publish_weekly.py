#!/usr/bin/env python3
"""Publish verified weekly recap to data/editorial.json; safe to rerun."""
import datetime,json,pathlib,urllib.request
BASE='https://api.sleeper.app/v1'; LEAGUE='1389751656299638784'; ROOT=pathlib.Path(__file__).resolve().parent

def get(path):
 req=urllib.request.Request(BASE+path,headers={'User-Agent':'HateReportPublisher/1.0'})
 with urllib.request.urlopen(req,timeout=25) as response:return json.load(response)

def main():
 state=get('/state/nfl'); current=int(state.get('week') or 1)
 # Publish the *completed* previous week, never invent results for the current week.
 completed=max(0,current-1)
 if completed<1:print('No completed week yet');return
 rosters=get(f'/league/{LEAGUE}/rosters');users=get(f'/league/{LEAGUE}/users');matches=get(f'/league/{LEAGUE}/matchups/{completed}')
 user={u['user_id']:u for u in users}
 names={r['roster_id']:r.get('metadata',{}).get('team_name') or user.get(r.get('owner_id'),{}).get('metadata',{}).get('team_name') or user.get(r.get('owner_id'),{}).get('display_name') or f"Team {r['roster_id']}" for r in rosters}
 grouped={}
 for m in matches:grouped.setdefault(m.get('matchup_id') or f"bye-{m['roster_id']}",[]).append(m)
 games=[g for g in grouped.values() if len(g)==2]
 stories=[]
 if games:
  winner=max((m for g in games for m in g),key=lambda m:m.get('points') or 0)
  stories.append({'title':'THE WEEK’S TOP SCORE','body':f"{names[winner['roster_id']]} posted {winner.get('points',0):.2f} points in Week {completed}."})
  close=min(games,key=lambda g:abs((g[0].get('points') or 0)-(g[1].get('points') or 0)))
  a,b=close;gap=abs((a.get('points') or 0)-(b.get('points') or 0))
  stories.append({'title':'PHOTO FINISH','body':f"{names[a['roster_id']]} and {names[b['roster_id']]} finished {gap:.2f} points apart ({a.get('points',0):.2f}–{b.get('points',0):.2f})."})
  blowout=max(games,key=lambda g:abs((g[0].get('points') or 0)-(g[1].get('points') or 0)))
  a,b=blowout;gap=abs((a.get('points') or 0)-(b.get('points') or 0))
  stories.append({'title':'NO MERCY','body':f"The widest margin was {gap:.2f} points: {names[a['roster_id']]} vs. {names[b['roster_id']]}."})
 out=ROOT/'data'/'editorial.json';out.parent.mkdir(parents=True,exist_ok=True)
 try: data=json.loads(out.read_text())
 except (FileNotFoundError,json.JSONDecodeError):data={'weeks':{}}
 data.setdefault('weeks',{})[str(completed)]={'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'stories':stories,'source':'Sleeper matchup results'}
 out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Published recap for Week {completed} ({len(stories)} verified stories)')
if __name__=='__main__':main()
