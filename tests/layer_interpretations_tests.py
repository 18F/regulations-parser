from regparser.layer.interpretations import Interpretations
from regparser.tree.struct import Node
from unittest import TestCase

class LayerInterpretationTest(TestCase):

    def test_process(self):
        root = Node(children = [
            Node("Interp11a", 
                [Node("child1"), Node("child2")],
                ['102', '11', 'a', Node.INTERP_MARK],
                node_type=Node.INTERP),
            Node("Interp11c5v", 
                label=['102', '11', 'c', '5', 'v', Node.INTERP_MARK],
                node_type=Node.INTERP),
            Node("InterpB5ii",
                label=['102','B','5','ii',Node.INTERP_MARK],
                node_type=Node.INTERP),
            Node(children=[Node(children=[
                Node("Interp9c1",
                    label=['102','9','c','1',Node.INTERP_MARK],
                    node_type=Node.INTERP)
                ], label=['102'])])
        ])

        interp = Interpretations(root)
        interp.pre_process()
        interp11a = interp.process(Node(label=['102', '11', 'a']))
        interp11c5v = interp.process(Node(
            label=['102', '11', 'c', '5', 'v']
        ))
        interpB5ii = interp.process(Node(label=['102','B','5','ii']))
        interp9c1 = interp.process(Node(label=['102', '9', 'c', '1']))
        
        self.assertEqual(1, len(interp11a))
        self.assertEqual(1, len(interp11c5v))
        self.assertEqual(1, len(interpB5ii))
        self.assertEqual(1, len(interp9c1))
        self.assertEqual('102-11-a-Interp', interp11a[0]['reference'])
        self.assertEqual('102-11-c-5-v-Interp', interp11c5v[0]['reference'])
        self.assertEqual('102-B-5-ii-Interp', interpB5ii[0]['reference'])
        self.assertEqual('102-9-c-1-Interp', interp9c1[0]['reference'])
        self.assertEqual(None, interp.process(Node(
            label=["102", "10", "a"])))

    def test_process_subparagraph_of_referenced_text(self):
        root = Node(children = [
            Node("\n\n\n", [   #   Empty
                 Node("Interp11a1",
                     label=['100','11','a','1',Node.INTERP_MARK],
                     node_type=Node.INTERP)],
                 label=['100', '11', 'a', Node.INTERP_MARK],
                 node_type=Node.INTERP)
        ], label=['100'])
        interp = Interpretations(root)
        interp.pre_process()
        self.assertEqual(None, interp.process(Node(
            label=['100', '11', 'a']
        )))
        self.assertFalse(interp.process(Node(
            label=['100', '11', 'a', '1'])) is None)

    def test_process_has_multiple_paragraphs(self):
        root = Node(children = [
            Node("\n\n\n",
                 [Node("Interp11a-1",
                      label=['100','11','a',Node.INTERP_MARK,'1'],
                      node_type=Node.INTERP)],
                 ['100', '11', 'a', Node.INTERP_MARK],
                 node_type=Node.INTERP)
            ], label=['100'])
        interp = Interpretations(root)
        interp.pre_process()
        self.assertFalse(interp.process(Node(
            label=["100", "11", "a"])) is None)

    def test_process_applies_to_multiple(self):
        i1a = Node('Text', title='Paragraph 1(a) and 1(b)',
                   label=['100', '1', 'a', Node.INTERP_MARK],
                   node_type=Node.INTERP)
        i1 = Node(label=['100', '1', Node.INTERP_MARK],
                  node_type=Node.INTERP, children=[i1a])
        root = Node(label=['100', Node.INTERP_MARK],
                    node_type=Node.INTERP, children=[i1])
        interp = Interpretations(root)
        interp.pre_process()
        self.assertFalse(interp.process(Node(label=['100', '1', 'a']))
                         is None)
        self.assertFalse(interp.process(Node(label=['100', '1', 'b']))
                         is None)

    def test_empty_interpretations(self):
        interp = Interpretations(None)
        self.assertTrue(interp.empty_interpretation(Node('\n\n')))
        self.assertTrue(interp.empty_interpretation(Node('',
            [Node('Subpar')])))
        self.assertFalse(interp.empty_interpretation(Node('Content')))
        self.assertFalse(interp.empty_interpretation(Node('',
            [Node('Something', label=['1', Node.INTERP_MARK, '3'])])))