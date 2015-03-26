# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl


class HomeRoot(epfl.components.CardinalLayout):
    def init_struct(self):
        for x in range(0, 10):
            node_list = []
            for y in range(0, 10):
                sub_node_list = []
                for z in range(0, 10):
                    sub_node_list.append(epfl.components.Box(
                        title='Box %s in Box %s in Box %s' % (z, y, x)
                    ))
                node_list.append(epfl.components.Box(
                    title='Box %s in Box %s' % (y, x),
                    node_list=sub_node_list
                ))
            self.node_list.append(epfl.components.Box(
                title='Box %s' % x,
                node_list=node_list
            ))


@view_config(route_name='home')
class HomePage(epfl.Page):
    root_node = HomeRoot(constrained=True)
