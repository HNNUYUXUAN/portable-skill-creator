import csv, importlib.util, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creator',ROOT/'scripts'/'creator.py'); c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
class Behavior(unittest.TestCase):
 def setUp(self): self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
 def tearDown(self): self.t.cleanup()
 def test_package_and_pairs(self): self.assertEqual(c.verify(ROOT)['status'],'pass')
 def test_export_without_workspace(self):
  dest=self.root/'中文 path';c.export(ROOT/'examples'/'json-to-csv',dest)
  out=self.root/'out.csv'
  subprocess.run([sys.executable,str(dest/'scripts'/'convert.py'),str(dest/'examples'/'input.json'),str(out)],cwd=self.root,check=True)
  with out.open(encoding='utf-8',newline='') as f:self.assertEqual(list(csv.DictReader(f))[0],{'name':'中文, item','count':'2'})
 def test_bad_input_creates_no_artifact(self):
  src=self.root/'bad.json';src.write_text('[{"name":"x","count":true}]');out=self.root/'out.csv'
  r=subprocess.run([sys.executable,str(ROOT/'examples/json-to-csv/scripts/convert.py'),str(src),str(out)],capture_output=True)
  self.assertNotEqual(r.returncode,0);self.assertFalse(out.exists())
 def test_escape(self):
  for x in ['../secret','C:/secret','x/../../secret']:
   with self.assertRaises(ValueError):c.safe(self.root,x)
 def test_existing_output_preserved(self):
  out=self.root/'existing.csv';out.write_text('original')
  r=subprocess.run([sys.executable,str(ROOT/'examples/json-to-csv/scripts/convert.py'),str(ROOT/'examples/json-to-csv/examples/input.json'),str(out)],capture_output=True,text=True)
  self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr);self.assertEqual(out.read_text(),'original')
 def test_allowlist_excludes_secrets(self):
  p=self.root/'package';c.export(ROOT/'examples/note-triage',p)
  (p/'.env').write_text('secret=synthetic')
  d=self.root/'export';c.export(p,d);self.assertFalse((d/'.env').exists())
  m=c.read(p/'delivery.json');m['files'].append('.env');c.write(p/'delivery.json',m)
  self.assertEqual(c.verify(p)['status'],'fail')
 def test_language_missing(self):
  p=self.root/'p';c.export(ROOT/'examples/note-triage',p);(p/'references/en/task.md').unlink()
  self.assertEqual(c.verify(p)['status'],'fail')
 def test_redaction(self):
  s=c.clean('token=SYNTHETIC https://example.com/file?signature=SYNTHETIC Authorization: Bearer SYNTHETIC')
  self.assertNotIn('SYNTHETIC',s)
 def test_upgrade_conflict_and_config(self):
  p=self.root/'installs'/'p';source=ROOT/'examples/note-triage';c.export(source,p)
  (p/'config.json').write_text('{"personal":true}')
  self.assertEqual(c.upgrade(source,p)['status'],'updated')
  self.assertTrue((p/'config.json').exists());self.assertTrue((c.backup_base(p)/'previous').exists())
  (p/'SKILL.md').write_text('user edited')
  self.assertEqual(c.upgrade(source,p)['status'],'conflict')
  r=subprocess.run([sys.executable,str(ROOT/'scripts/creator.py'),'rollback',str(p)],capture_output=True)
  self.assertEqual(r.returncode,0)
  self.assertEqual(c.digest(p/'SKILL.md'),c.digest(source/'SKILL.md'))
  self.assertEqual((c.backup_base(p)/'rolled-back'/'SKILL.md').read_text(),'user edited')
 def test_resume_unknown(self):
  from argparse import Namespace
  p=self.root/'session'
  args=Namespace(path=str(p),action='start',goal='test',host='test',model='unknown',event=None);c.session(args)
  e=self.root/'event.json';c.write(e,{'step':'CAP-1','status':'unknown','summary':'token=SYNTHETIC','raw_output':'NEVER_STORE'})
  args.action='record';args.event=str(e);c.session(args)
  args.action='resume';r=c.session(args);self.assertEqual(len(r['unresolved']),1)
  self.assertNotIn('SYNTHETIC',(p/'events.jsonl').read_text());self.assertNotIn('NEVER_STORE',(p/'events.jsonl').read_text())
 def test_deleted_install_is_conflict(self):
  p=self.root/'installs'/'deleted';source=ROOT/'examples/note-triage';c.export(source,p)
  (p/'SKILL.md').unlink()
  self.assertEqual(c.upgrade(source,p),{'status':'conflict','files':['SKILL.md']})
  self.assertFalse((p/'SKILL.md').exists())
 def test_jianying_static_patterns(self):
  p=self.root/'fixture';p.mkdir();(p/'x.py').write_text('dotenv_values("D:/data/.env")\nplatform="win32"\ndll="videoeditor.dll"\n')
  kinds={f['type'] for f in c.inspect(p)['findings']}
  self.assertTrue({'absolute_path','dotenv','windows_binary'}<=kinds)
if __name__=='__main__':unittest.main()
