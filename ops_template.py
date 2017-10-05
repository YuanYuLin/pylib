#from jinja2 import Environment, FileSystemLoader
from bottle import SimpleTemplate
'''
def parseTemplate(template_dir, template_name, project_data):
  env = Environment(loader=FileSystemLoader(template_dir))
  env.globals['OSSEP'] = ossep()
  env.globals['SPICES'] = includespices
  env.globals['BUGON'] = bugon
  env.globals['DEBUG'] = debug
  print "(----------------------------)"
  pprint.pprint(project_data)
  print "[===========================]"
  result = env.get_template(template_name).render(project_data)
  return result

def saveTemplate(templateResult, output_dir, output_file):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    w_path = output_dir + os.sep + output_file
    with open(w_path, 'w') as fd:
      fd.write(templateResult)

def parseAndSaveTemplate(in_tmpl_dir, in_tmpl_name, out_dir, out_name, data):
  result = parseTemplate(in_tmpl_dir, in_tmpl_name, data)
  saveTemplate(result, out_dir, out_name)
'''
def generateTemplateByFile(template_file, template_obj):
  tmpl = SimpleTemplate(name=template_file)
  output = tmpl.render(root_obj=template_obj)

  return output

def generateTemplateByText(template_text, template_obj):
  tmpl = SimpleTemplate(template_text)
  output = tmpl.render(root_obj=template_obj)

  return output
