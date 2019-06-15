var nodes = [...baseNodes];
var links = [...baseLinks];

//console.log(nodes)

var width = window.innerWidth; 
var height = window.innerHeight;
var radius = 12;

var svg = d3.select('svg');
svg.attr('width', width).attr('height', height); // fills window

// define additional selection functionalities
function getNeighbors(node) {
    return baseLinks.reduce((neighbors, link) => {
        if (link.target.id === node.id) {
            neighbors.push(link.source.id)
        } else if (link.source.id === node.id) {
            neighbors.push(link.target.id)
        }
        return neighbors
    }, [node.id])
}

function isNeighborLink(node,link) {
    return link.target.id === node.id || link.source.id === node.id
}

function getNodeColor(node, neighbors) {
    if (neighbors instanceof Array && neighbors.indexOf(node.id) > -1) {
        return node.level === 0 ? '#e1fb39' : 'orange'
    }
    return node.level === 0 ? '#a6fb39' : 'gray' 
}

function getTextColor(node, neighbors) {
    if (node.level == 0) {
        return neighbors.indexOf(node.id) > -1 ? '#e1fb39' : '#a6fb39'
    }
    return neighbors.indexOf(node.id) > -1 ? 'orange' : 'white'
}

function getLinkColor(node, link) {
    //console.log("checking link color");
    return isNeighborLink(node, link) ? 'orange' : '#E5E5E5'
}
// Simulation setup
var simulation = d3
    .forceSimulation() // creates force simulation instance
    .force('charge', d3.forceManyBody().strength(-120)) // creates repulsive effects between nodes
    .force('center', d3.forceCenter(width/2, height/2)); // creates automatic re-centering effects

simulation.force('link', d3.forceLink() // adds link force to simulation
    .id(link => link.id)
    .strength(link => link.strength));

var dragDrop = d3.drag()
    .on('start', node => {
        node.fx = node.x;
        node.fy = node.y;
    })
    .on('drag', node => {
        simulation.alphaTarget(0.2).restart();
        node.fx = d3.event.x;
        node.fy = d3.event.y;
    })
    .on('end', node => {
        if (!d3.event.active) {
            simulation.alphaTarget(0)
        }
        node.fx = null;
        node.fy = null;
    })

function selectNode(selectedNode) {
    if (selectedNode.id === selectedId) { // no change in selected node
        selectedId = undefined;
        resetData();
        updateSimulation();
    } else { // change in selected node
        selectedId = selectedNode.id;
        updateData(selectedNode);
        updateSimulation();
    }
    var neighbors = getNeighbors(selectedNode);
    //console.log(neighbors);

    nodeElements.attr('fill', node => getNodeColor(node, neighbors));
    textElements.attr('fill', node => getTextColor(node, neighbors));
    linkElements.attr('stroke', link => getLinkColor(selectedNode, link));
}

function resetData() {
    var nodeIds = nodes.map(node => node.id);

    baseNodes.forEach(node => {
        if (nodeIds.indexOf(node.id) === -1) { // missing nodes
            nodes.push(node); // replaces missing nodes
        }
    })

    links = baseLinks;
}

var nodeGroup = svg.append("g").attr("class", "nodes");
var textGroup = svg.append("g").attr("class", "texts");
var linkGroup = svg.append("g").attr("class", "links");

let nodeElements, textElements, linkElements, imgElements;

var selectedId;

function updateGraph() {
    // update nodes
    nodeElements = nodeGroup 
        .selectAll('image')
        .data(nodes, node => node.id); // binds circles to nodes created
    
    nodeElements.exit().remove(); // selects and removes elements that need to be removed
    
    const nodeEnter = nodeElements
        .enter()
        .append('svg:image') // start
        .attr('class', 'circle')
        .attr('xlink:href', node => (node.img != null) ? node.img : "https://opengameart.org/sites/default/files/styles/medium/public/Transparency100.png")
        .attr('stroke', '#E5E5E5')
        .attr('stroke-width', 3)
        .attr('height', radius*2)
        .attr('width', radius*2)
        .call(dragDrop)
        .on('click', selectNode);
    
    /*
    const nodeEnter = nodeElements
        .enter()
        .append('circle') // creates circles for nodes without a circle element
        .attr('r', radius)
        .attr('fill', node => (node.img != null) ? 'url(#node.img)' : "https://opengameart.org/sites/default/files/styles/medium/public/Transparency100.png")
        //.attr('fill', node => getNodeColor(node))
        .attr('stroke', node => d3.rgb(getNodeColor(node)).darker())
        .call(dragDrop)
        .on('click', selectNode);
    */
    nodeElements = nodeEnter.merge(nodeElements);

    // update texts
    textElements = textGroup
        .selectAll('text')
        .data(nodes, node => node.id);
    
    textElements.exit().remove();
    
    const textEnter = textElements
        .enter()
        .append('text')
        .text(node => node.label)
        .attr('font-size', 7)
        .attr('dx', 25) // defines position of label
        .attr('dy', 15) // defines position of label
        .attr('fill', node => getTextColor(node, []));
    
    textElements = textEnter.merge(textElements);

    // update links
    linkElements = linkGroup
        .selectAll('line')
        .data(links, link => {
            return link.target.id + link.source.id
        });
    
    linkElements.exit().remove();

    const linkEnter = linkElements
        .enter()
        .append('line')
        .attr('stroke-width', 1)
        .attr('stroke', '#E5E5E5');
    
    linkElements = linkEnter.merge(linkElements);
}

function updateSimulation() {
    updateGraph();

    simulation.nodes(nodes).on('tick', () => {
        /*
         // Use this to prevent nodes from flying out of bounds
        nodeElements
            .attr("cx", node => Math.max(radius, Math.min(width - radius, node.x))) 
            .attr("cy", node => Math.max(radius, Math.min(height - radius, node.y)));
        */
        // Use this to let nodes fly around freely
        nodeElements
            .attr("x", node => node.x) 
            .attr("y", node => node.y);
        textElements
            .attr("x", node => node.x)
            .attr("y", node => node.y);
        linkElements
            .attr('x1', link => link.source.x+radius)
            .attr('y1', link => link.source.y+radius)
            .attr('x2', link => link.target.x+radius)
            .attr('y2', link => link.target.y+radius);
    });

    simulation.force('link').links(links);
    simulation.alphaTarget(0.2).restart();
}

// getting difference and mutating the data
function updateData(selectedNode) {
    const neighbors = getNeighbors(selectedNode);

    const newNodes = baseNodes.filter(node => {
        return neighbors.indexOf(node.id) > -1 || node.level === 1 // filter out nodes that are not neighbors; keeps neighboring nodes
    })

    const difference = {
        // to be removed
        removed: nodes.filter(node => newNodes.indexOf(node) === -1), // filter out non-new neighbor nodes -> to be removed
        // to be added
        added: newNodes.filter(node => nodes.indexOf(node) === -1) // filter out new neighboring nodes that are not currently present
    }

    difference.removed.forEach(node => nodes.splice(nodes.indexOf(node), 1));
    difference.added.forEach(node => nodes.push(node));

    links = baseLinks.filter(link => {
        return link.target.id === selectedNode.id || link.source.id === selectedNode.id
    })
}

updateSimulation();