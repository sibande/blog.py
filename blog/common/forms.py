from web import form

post_form = form.Form(
    form.Textbox('title',
                 form.notnull,
                 class_='title',
                 description='Title'), 
    form.Textarea('body',
                  form.notnull,
                  class_="post",
                  description='Body'),
    form.Checkbox('active', description='Active'),
    form.Button('Post'),
)

static_form = form.Form(
    form.Textbox('position',
                 form.notnull,
                 form.regexp('\d+', 'Must be a digit'),
                 class_='text',
                 description='Position number'),
    form.Textbox('name',
                 form.notnull,
                 class_='text',
                 description='Name (absolute page path)'),
    form.Textbox('label',
                 form.notnull,
                 class_='text',
                 description='Link label'),
    form.Textbox('title',
                 class_='text',
                 description='Full page label'),
    form.Textarea('content',
                 form.notnull,
                 class_='text',
                 description='Content'),
    form.Checkbox('active', description='Active'),
    form.Button('Post'),
)
