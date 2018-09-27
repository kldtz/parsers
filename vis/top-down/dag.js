d3.json("dag-data/a-a-b-b-a-b-lexicographic.json", function (data) {
    var goals = [];
    var nodes = {};
    console.log(nodes);
    for (let node of data) {
        if (node.isGoal) {
            goals.push(node);
        }
        nodes[node.id] = node;
    }
    for (let goal of goals) {
        markPath(nodes, goal);
    }
    drawGraph(data);
});

function markPath(nodes, node) {
    node['isGoalPath'] = true;
    for (let parent of node.parents) {
        if (!parent) {
            continue;
        }
        markPath(nodes, nodes[parent]);
    }
}

function drawGraph(data) {
    // Create the input graph
    var g = new dagreD3.graphlib.Graph()
        .setGraph({ rankdir: 'LR', ranksep: 20, edgesep: 0, nodesep: 10 })
        .setDefaultEdgeLabel(function () { return {}; });

    for (let node of data) {
        let classLabel = (node.rule || node.parents[0] == null ? "predict" : "match") +
            '-' + (node.isGoalPath ? 'goal-path' : 'non-goal-path');
        g.setNode(node.id, {
            label: node.position + (node.prediction.length > 0 ? ':' + node.prediction.join('') : ''),
            shape: "rect", "class": classLabel
        });
        for (let parentId of node.parents) {
            if (parentId === null) continue;
            g.setEdge(parentId, node.id);
        }
    }

    g.nodes().forEach(function (v) {
        var node = g.node(v);
        // Round the corners of the nodes
        node.rx = node.ry = 5;
    });

    // Create the renderer
    var render = new dagreD3.render();

    // Set up an SVG group so that we can translate the final graph.
    var svg = d3.select("svg"),
        svgGroup = svg.append("g");

    // Run the renderer. This is what draws the final graph.
    render(d3.select("svg g"), g);

    // Center the graph
    var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
    svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
    svg.attr("height", g.graph().height + 40);
}
