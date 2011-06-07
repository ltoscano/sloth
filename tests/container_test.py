from sloth.annotations.container import *

class MockupContainer:
    pass

def someFileAnnotations(i):
    annotations = []
    annotations.append({'type': 'rect',
                        'x': 10 * i,
                        'y': '20',
                        'w': '40',
                        'h': '60'})
    annotations.append({'type': 'rect',
                        'x': '80',
                        'y': 20 * i,
                        'w': '40',
                        'h': '60'})
    for k in range(i):
        annotations.append({'type': 'point',
                            'x': 30 * k,
                            'y': 30 * k})
    return annotations

def someAnnotations():
    annotations = []
    for i in range(5):
        file = {
            'filename': 'file%d.png' % i,
            'type': 'image',
            'annotations': someFileAnnotations(i)
        }
        annotations.append(file)
    return annotations

def common_container_test(filename, container):
    original_anns = someAnnotations()

    container.setAnnotations(original_anns)
    assert len(container.annotations()) == len(original_anns)

    container.save(filename)
    assert container.filename() == filename
    assert os.path.exists(filename)

    container.clear()
    assert container.filename() is None
    assert len(container.annotations()) == 0

    container.load(filename)
    assert container.filename() == filename
    assert len(container.annotations()) == len(original_anns)

def test_import_callable():
    containers = (('*', 'container_test.MockupContainer'),)
    factory = AnnotationContainerFactory(containers)
    item = factory.create('test')
    assert isinstance(item, MockupContainer)

def test_PickleContainer(tmpdir):
    filename = os.path.join(str(tmpdir), "test_PickleContainer.pickle")
    container = PickleContainer()
    common_container_test(filename, container)

def test_JsonContainer(tmpdir):
    filename = os.path.join(str(tmpdir), "test_JsonContainer.json")
    container = JsonContainer()
    common_container_test(filename, container)

def test_YamlContainer(tmpdir):
    filename = os.path.join(str(tmpdir), "test_YamlContainer.yaml")
    container = YamlContainer()
    common_container_test(filename, container)
