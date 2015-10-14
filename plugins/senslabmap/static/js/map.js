var Senslab = {
  normalize: function(node) {
    var info;
    
    if (node.component_name) { // wsn430-11.devlille.iot-lab.info
      info = node.component_name.split(".");
    } /*else if (node.hrn) { // iotlab.a8-11\.devgrenoble\.iot-lab\.info
      var info = node.hrn.split("\\.");
      info[0] = info[0].split(".")[1];
    }*/

    if (info && info[2] == "iot-lab" && info[3] == "info") {
      node.arch = info[0].split("-")[0];
      node.id = parseInt(info[0].split("-")[1]);
      node.site = info[1];
      node.x = parseFloat(node.x);
      node.y = parseFloat(node.y);
      node.z = parseFloat(node.z);
      node.selected = false;
      node.normalized = true;
    }
  },
  notify: function(node) {
    console.log("[Notify] node " + node.id + " is " + node.selected);
  },
  createMaps: function($container, sites, nodes) {
    var maps = {};
    var $menu = $("<ul id='sites-tabs' class='nav nav-tabs' data-tabs='sites-tabs'/>").appendTo($container);
    var $maps = $("<div id='maps' class='tab-content' />").appendTo($container);
    
    $.each(sites, function(i, site) {
      var entry = $("<li><a href='#" + site + "' data-toggle='tab'>" + site + "</a></li>").appendTo($menu);
      var $tab = $("<div class='tab-pane' id='" + site + "' />").appendTo($maps);
      maps[site] = new Senslab.Map($tab);
      maps[site].addNodes(nodes[site]);
    });
    
    $menu.find("li").eq(0).addClass("active");
    $maps.find("div").eq(0).addClass("active");

    if (!sites.length) {
      $container.text("No nodes to display.");
    }
  }
};

Senslab.Map = function() {
  var colors = {
    "Alive": 0x7FFF00,
    "Busy": 0x9943BE,
    "Suspected": 0xFF3030,
    "Selected": 0x0099CC
  };

  var archs = [
    "wsn430",
    "m3",
    "a8"
  ];
  
  function Map($container, options) {
    this.width  = 600;
    this.height = 400;
    
    this.distance = 50;
    this.phi = -100;
    this.theta = 0;
    this.onRot = false;
    
    this.pointerDetectRay = new THREE.Raycaster();
    this.pointerDetectRay.ray.direction.set(0, -1, 0);
    this.projector = new THREE.Projector();
    this.mouse2D = new THREE.Vector3(0, 0, 0);
    
    this.renderer = new THREE.CanvasRenderer();
    this.renderer.setSize(this.width, this.height);
    
    this.camera = new THREE.PerspectiveCamera(75, this.width / this.height, 1, 10000);
    
    this.scene = new THREE.Scene();
    this.scene.add(this.camera);
    
    this.updatePosition();
    
    var self = this;
    
    this.$nodeInputs = {};
    
    $.each(archs, function(i, arch) {
      self.$nodeInputs[arch] = $("<input type='text' placeholder='" + arch + "'>")
      .appendTo($container)
      .change(function() {
        self.updateSelected(arch, expand($(this).val()));
        self.update();
      });
    });
    
    var $canvas = $(this.renderer.domElement)
    .mousemove(function(e) {
      self.mouse2D.x =  ((e.pageX - $canvas.offset().left) / $canvas.width()) * 2 - 1;
      self.mouse2D.y = -((e.pageY - $canvas.offset().top) / $canvas.height()) * 2 + 1;
      
      if (self.onRot) {
        self.theta -= e.pageX - self.mouse2D.pageX;
        self.phi += e.pageY - self.mouse2D.pageY;
        if (self.phi > 180)
          self.phi = 180;
        if (self.phi < -180)
          self.phi = -180;
        
        self.mouse2D.pageX = e.pageX;
        self.mouse2D.pageY = e.pageY;
        
        self.updatePosition();
        self.update();
      }
    }).mousedown(function(e) {
      e.preventDefault();
      switch (e.which) {
        case 1:
          self.pointerDetectRay = self.projector.pickingRay(self.mouse2D.clone(), self.camera);
          var intersects = self.pointerDetectRay.intersectObjects(self.scene.children);
          if (intersects.length > 0) {
            var particle = intersects[0].object;
            if (particle.data.boot_state != "Suspected") {
              setSelected(particle, !particle.data.selected);
              var $nodeInput = self.$nodeInputs[particle.data.arch];
              $nodeInput.val(factorize(self.getNodesId(particle.data.arch)));
              self.update();
            }
          }
          break;
        case 3:
          self.mouse2D.pageX = e.pageX;
          self.mouse2D.pageY = e.pageY;
          self.onRot = true;
          break;
      }
    }).mouseup(function(e) {
      e.preventDefault();
      switch (e.which) {
        case 3:
          self.onRot = false;
          break;
      }
    }).mouseleave(function(e) {
      self.onRot = false;
    }).mousewheel(function(e, delta) {
      e.preventDefault();
      self.distance += delta * 5;
      self.updatePosition();
      self.update();
    });
    
    $container.append($canvas);
  }
  
  Map.prototype.getNodesId = function(arch) {
    var particles = this.scene.children;
    var nodes = [];
    for (var i = 0; i < particles.length; ++i) {
      if (particles[i].data && particles[i].data.arch == arch && particles[i].data.selected) {
        nodes.push(particles[i].id);
      }
    }
    return nodes;
  }
  
  Map.prototype.addNodes = function(nodes) {
    var center = getCenter(nodes);

    nodes.sort(function(a, b) {
      return a.id - b.id;
    });
    
    for(var i = 0; i < nodes.length; ++i) {
      var material = new THREE.ParticleCanvasMaterial({program: circle});
      var particle = new THREE.Particle(material);
      particle.data = nodes[i];
      particle.id = parseInt(nodes[i].id);
      particle.position.x = (nodes[i].x - center.x) * 10;
      particle.position.y = (nodes[i].y - center.y) * 10;
      particle.position.z = (nodes[i].z - center.z) * 10;
      particle.scale.x = particle.scale.y = 1;
      setColor(particle)
      this.scene.add(particle);
    }
    this.update();
  };
  
  Map.prototype.updateSelected = function(arch, selectedNodes) {
    var particles = this.scene.children;
    for (var i = 0; i < particles.length; ++i) {
      if (particles[i].data && particles[i].data.arch == arch && particles[i].data.boot_state != "Suspected") {
        var particle = particles[i];
        var selected = $.inArray(particle.id, selectedNodes) != -1;
        if (particle.data.selected != selected) {
          setSelected(particle, selected);
        }
      }
    }
  }
  
  Map.prototype.updatePosition = function() {
    this.camera.position.x = this.distance
      * Math.sin(this.theta * Math.PI / 360)
      * Math.cos(this.phi * Math.PI / 360);
    this.camera.position.y = this.distance * Math.sin(this.phi * Math.PI / 360);
    this.camera.position.z = this.distance
      * Math.cos(this.theta * Math.PI / 360)
      * Math.cos(this.phi * Math.PI / 360);
    this.camera.lookAt(this.scene.position);
    this.camera.updateMatrix();
  };
  
  Map.prototype.update = function() {
    this.renderer.render(this.scene, this.camera);
  };

  function setSelected(particle, selected) {
    particle.data.selected = selected;
    setColor(particle);
    Senslab.notify(particle.data);
  }

  function setColor(particle) {
    var color = particle.data.selected ? colors["Selected"] : colors[particle.data.boot_state];
    particle.material.color.setHex(color);
  }

  function getCenter(nodes) {
    var xmin = 0, ymin = 0, zmin = 0;
    var xmax = 0, ymax = 0, zmax = 0;
    
    for (var i = 0; i < nodes.length; ++i) {
      if (nodes[i].x > xmax) xmax = nodes[i].x;
      if (nodes[i].x < xmin) xmin = nodes[i].x;
      if (nodes[i].y > ymax) ymax = nodes[i].y;
      if (nodes[i].y < ymin) ymin = nodes[i].y;
      if (nodes[i].z > zmax) zmax = nodes[i].z;
      if (nodes[i].z < zmin) zmin = nodes[i].z;
    }
    return {x: (xmax + xmin) / 2, y: (ymax + ymin) / 2, z: (zmax + zmin) / 2};
  }

  function factorize(nodes) {
    var factorized = [];
    var prev = 0;
    var intervalStart = 0;
    
    for (var i = 0; i < nodes.length; ++i) {
      if (intervalStart) {
        if (nodes[i] == prev + 1) {
          prev++;
        } else {
          factorized.push(intervalStart + "-" + prev);
          intervalStart = 0;
          prev = nodes[i];
        }
      } else {
        if (nodes[i] == prev + 1) {
          intervalStart = prev;
          prev++;
        } else {
          prev && factorized.push(prev);
          prev = nodes[i];
        }
      }
    }
    factorized.push(intervalStart ? intervalStart + "-" + prev : prev);
    return factorized.join(",");
  }
  
  function expand(input) {
    var factorized = input.split(",");
    var expanded = [];
    for (var i = 0; i < factorized.length; ++i) {
      var d = factorized[i].split("-");
      if (d.length == 2) {
        for (var j = parseInt(d[0]); j < parseInt(d[1]) + 1; j++) {
          expanded.push(j);
        }
      } else {
        expanded.push(parseInt(factorized[i]));
      }
    }
    
    expanded.sort(function(a, b) {
      return a - b;
    });
    
    for (var i = 1; i < expanded.length; i++) {
      if (expanded[i] == expanded[i - 1]) {
        expanded.splice(i--, 1);
      }
    }
    return expanded;
  }

  function circle(context) {
    context.beginPath();
    context.arc(0, 0, 1, 0, Math.PI * 2, true);
    context.closePath();
    context.fill();
  };
  
  return Map;
}();