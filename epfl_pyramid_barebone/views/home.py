# * encoding: utf-8
import time
from pyramid.view import view_config
from solute import epfl


class DebugBox(epfl.components.Box):
    def render(self, target='main'):
        debug_dict['calls'] += 1
        return super(DebugBox, self).render(target=target)

    def render_templates(self, env, templates):
        start_time = time.time()
        out = super(DebugBox, self).render_templates(env, templates)
        debug_dict.setdefault(self.cid, {}).setdefault('render_templates_time', 0)
        debug_dict.setdefault(self.cid, {}).setdefault('render_templates_calls', 0)
        debug_dict[self.cid]['render_templates_time'] += time.time() - start_time
        debug_dict[self.cid]['render_templates_calls'] += 1
        return out


class HomeRoot(epfl.components.CardinalLayout):
    def init_struct(self):
        for x in range(0, 10):
            node_list = []
            for y in range(0, 10):
                sub_node_list = []
                for z in range(0, 10):
                    sub_node_list.append(DebugBox(
                        title='Box %s in Box %s in Box %s' % (z, y, x)
                    ))
                node_list.append(DebugBox(
                    title='Box %s in Box %s' % (y, x),
                    node_list=sub_node_list
                ))
            self.node_list.append(DebugBox(
                title='Box %s' % x,
                node_list=node_list
            ))

    def render(self, target='main'):
        debug_dict['calls'] += 1
        return super(HomeRoot, self).render(target=target)


@view_config(route_name='home')
class HomePage(epfl.Page):
    root_node = HomeRoot(constrained=True)

    def __init__(self, request, transaction=None):
        debug_dict['init_start_time'] = time.time()
        super(HomePage, self).__init__(request, transaction=transaction)
        debug_dict['init_end_time'] = time.time()

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        out = super(HomePage, self).__call__(*args, **kwargs)
        end_time = time.time()

        render_end_time = debug_dict.pop('render_end_time')
        render_start_time = debug_dict.pop('render_start_time')

        init_end_time = debug_dict.pop('init_end_time')
        init_start_time = debug_dict.pop('init_start_time')

        calls = debug_dict.pop('calls')
        render_templates_time = 0
        render_templates_calls = 0
        for k, v in debug_dict.iteritems():
            render_templates_time += v['render_templates_time']
            render_templates_calls += v['render_templates_calls']

        call_time = render_end_time - render_start_time
        data = [
            ("render calls total", calls, ),
            ("render time total", render_end_time - render_start_time, ),
            ("render time per call", call_time / calls, ),
            ("render_templates calls total", render_templates_calls, ),
            ("render_templates time total", render_templates_time, ),
            ("render_templates time per call", render_templates_time / render_templates_calls, ),
            ("__init__ time total", init_end_time - init_start_time, ),
            ("__call__ time total", end_time - start_time, ),
        ]
        data_out = []
        data_length = 0
        for v in data:
            data_out.append("| {:<30} | {:<30} |".format(*v))
            data_length = max(data_length, len(data_out[-1]))

        print "=" * data_length
        print "\n".join(data_out)
        print "=" * data_length

        debug_dict.clear()
        debug_dict.update({
            'calls': 0,
            'render_start_time': 0,
            'render_end_time': 0
        })
        return out

    def render(self):
        debug_dict['render_start_time'] = time.time()
        out = super(HomePage, self).render()
        debug_dict['render_end_time'] = time.time()
        return out

debug_dict = {
    'calls': 0,
    'render_start_time': 0,
    'render_end_time': 0,
    'init_start_time': 0,
    'init_end_time': 0
}