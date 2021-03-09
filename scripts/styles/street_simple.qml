<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="1" readOnly="0" styleCategories="AllStyleCategories" simplifyAlgorithm="0" maxScale="0" minScale="100000000" simplifyDrawingHints="1" simplifyDrawingTol="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyMaxScale="1" version="3.14.1-Pi">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startField="" accumulate="0" mode="0" endField="" durationUnit="min" fixedDuration="0" endExpression="" durationField="" enabled="0" startExpression="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" enableorderby="0" attr="highway" type="categorizedSymbol" symbollevels="0">
    <categories>
      <category value="construction" render="true" symbol="0" label="construction"/>
      <category value="" render="true" symbol="1" label=""/>
    </categories>
    <symbols>
      <symbol clip_to_extent="1" type="line" force_rhr="0" name="0" alpha="1">
        <layer class="MarkerLine" pass="0" enabled="1" locked="0">
          <prop v="4" k="average_angle_length"/>
          <prop v="3x:0,0,0,0,0,0" k="average_angle_map_unit_scale"/>
          <prop v="MM" k="average_angle_unit"/>
          <prop v="4" k="interval"/>
          <prop v="3x:0,0,0,0,0,0" k="interval_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="interval_unit"/>
          <prop v="0" k="offset"/>
          <prop v="0" k="offset_along_line"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_along_line_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_along_line_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="RenderMetersInMapUnits" k="offset_unit"/>
          <prop v="interval" k="placement"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="rotate"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="interval">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="&quot;width_proc&quot;" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="&quot;width_proc&quot; / 4" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" type="marker" force_rhr="0" name="@0@0" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop v="0" k="angle"/>
              <prop v="210,210,210,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="no" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option type="Map" name="properties">
                    <Option type="Map" name="size">
                      <Option value="true" type="bool" name="active"/>
                      <Option value="&quot;width_proc&quot; / 2" type="QString" name="expression"/>
                      <Option value="3" type="int" name="type"/>
                    </Option>
                  </Option>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="line" force_rhr="0" name="1" alpha="1">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
          <prop v="round" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MapUnit" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="round" k="joinstyle"/>
          <prop v="210,210,210,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MapUnit" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MapUnit" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="offset">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="(to_real(&quot;parking:lane:right:width:carriageway&quot;) - to_real(&quot;parking:lane:left:width:carriageway&quot;)) / 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="&quot;width_proc&quot;" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" type="line" force_rhr="0" name="0" alpha="1">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
          <prop v="round" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MapUnit" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="round" k="joinstyle"/>
          <prop v="210,210,210,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MapUnit" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MapUnit" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="processing_width" type="QString" name="field"/>
                  <Option value="2" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontCapitals="0" allowHtml="0" fontKerning="1" namedStyle="Book" textOrientation="horizontal" fontFamily="DejaVu Sans" fontWordSpacing="0" fieldName="name" blendMode="0" fontWeight="50" fontSize="10" fontItalic="0" multilineHeight="1" useSubstitutions="0" previewBkgrdColor="255,255,255,255" isExpression="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="255,255,255,255" fontSizeUnit="RenderMetersInMapUnits" fontUnderline="0" fontStrikeout="0" textOpacity="1" fontLetterSpacing="0">
        <text-buffer bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferColor="255,255,255,255" bufferSizeUnits="MM" bufferDraw="0" bufferBlendMode="0" bufferJoinStyle="128" bufferOpacity="1" bufferSize="1"/>
        <text-mask maskJoinStyle="128" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskEnabled="0" maskSize="1.5" maskOpacity="1" maskType="0" maskSizeUnits="MM"/>
        <background shapeOffsetY="0" shapeSizeUnit="MM" shapeRotation="0" shapeBorderWidth="0" shapeSizeType="0" shapeRotationType="0" shapeBlendMode="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeY="0" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeSVGFile="" shapeOffsetX="0" shapeBorderWidthUnit="MM" shapeSizeX="0" shapeDraw="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeOffsetUnit="MM" shapeRadiiUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64">
          <symbol clip_to_extent="1" type="marker" force_rhr="0" name="markerSymbol" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop v="0" k="angle"/>
              <prop v="232,113,141,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowRadiusUnit="MM" shadowColor="0,0,0,255" shadowDraw="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowOpacity="0.7" shadowBlendMode="6" shadowOffsetAngle="135" shadowOffsetGlobal="1" shadowScale="100" shadowUnder="0" shadowOffsetUnit="MM"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format multilineAlign="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" leftDirectionSymbol="&lt;" autoWrapLength="0" addDirectionSymbol="0" decimals="3" useMaxLineLengthForAutoWrap="1"/>
      <placement labelOffsetMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" centroidWhole="0" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" layerType="LineGeometry" placement="3" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" maxCurvedCharAngleOut="-25" placementFlags="9" geometryGenerator="" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" polygonPlacementFlags="2" distMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" dist="0" xOffset="0" overrunDistance="0" repeatDistanceUnits="RenderMetersInMapUnits" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" quadOffset="4" preserveRotation="1" yOffset="0" priority="5" repeatDistance="250" offsetUnits="MM" distUnits="MM" rotationAngle="0" fitInPolygonOnly="0"/>
      <rendering limitNumLabels="0" obstacleFactor="1" obstacleType="1" obstacle="1" fontMinPixelSize="3" scaleMin="0" drawLabels="1" fontMaxPixelSize="10000" zIndex="0" displayAll="0" fontLimitPixelSize="0" maxNumLabels="2000" minFeatureSize="0" scaleVisibility="0" mergeLines="1" scaleMax="0" upsidedownLabels="0" labelPerPart="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option type="Map" name="properties">
            <Option type="Map" name="Size">
              <Option value="true" type="bool" name="active"/>
              <Option value="&quot;processing_width&quot; - 2" type="QString" name="expression"/>
              <Option value="3" type="int" name="type"/>
            </Option>
          </Option>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
          <Option type="Map" name="ddProperties">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
          <Option value="false" type="bool" name="drawToAllParts"/>
          <Option value="0" type="QString" name="enabled"/>
          <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
          <Option value="&lt;symbol clip_to_extent=&quot;1&quot; type=&quot;line&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
          <Option value="0" type="double" name="minLength"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
          <Option value="MM" type="QString" name="minLengthUnit"/>
          <Option value="0" type="double" name="offsetFromAnchor"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
          <Option value="0" type="double" name="offsetFromLabel"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory height="15" sizeType="MM" barWidth="5" spacingUnit="MM" lineSizeType="MM" penColor="#000000" backgroundAlpha="255" opacity="1" direction="0" labelPlacementMethod="XHeight" rotationOffset="270" showAxis="1" scaleBasedVisibility="0" penWidth="0" enabled="0" spacingUnitScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+8" minScaleDenominator="0" diagramOrientation="Up" penAlpha="255" width="15" minimumSize="0" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" sizeScale="3x:0,0,0,0,0,0" spacing="5">
      <fontProperties description="Cantarell,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol clip_to_extent="1" type="line" force_rhr="0" name="" alpha="1">
          <layer class="SimpleLine" pass="0" enabled="1" locked="0">
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" zIndex="0" priority="0" obstacle="0" placement="2" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <referencedLayers/>
  <referencingLayers/>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="surface">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width_proc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width_proc:effective">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:position">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:position">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:width:carriageway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:width:carriageway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:offset">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:offset">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="error_output">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="highway" index="1" name=""/>
    <alias field="name" index="2" name=""/>
    <alias field="surface" index="3" name=""/>
    <alias field="parking:lane:left" index="4" name=""/>
    <alias field="parking:lane:right" index="5" name=""/>
    <alias field="width_proc" index="6" name=""/>
    <alias field="width_proc:effective" index="7" name=""/>
    <alias field="parking:lane:left:position" index="8" name=""/>
    <alias field="parking:lane:right:position" index="9" name=""/>
    <alias field="parking:lane:left:width" index="10" name=""/>
    <alias field="parking:lane:right:width" index="11" name=""/>
    <alias field="parking:lane:left:width:carriageway" index="12" name=""/>
    <alias field="parking:lane:right:width:carriageway" index="13" name=""/>
    <alias field="parking:lane:left:offset" index="14" name=""/>
    <alias field="parking:lane:right:offset" index="15" name=""/>
    <alias field="error_output" index="16" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="id"/>
    <default applyOnUpdate="0" expression="" field="highway"/>
    <default applyOnUpdate="0" expression="" field="name"/>
    <default applyOnUpdate="0" expression="" field="surface"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:left"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:right"/>
    <default applyOnUpdate="0" expression="" field="width_proc"/>
    <default applyOnUpdate="0" expression="" field="width_proc:effective"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:left:position"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:right:position"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:left:width"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:right:width"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:left:width:carriageway"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:right:width:carriageway"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:left:offset"/>
    <default applyOnUpdate="0" expression="" field="parking:lane:right:offset"/>
    <default applyOnUpdate="0" expression="" field="error_output"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="id" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="highway" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="name" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="surface" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:left" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:right" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="width_proc" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="width_proc:effective" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:left:position" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:right:position" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:left:width" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:right:width" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:left:width:carriageway" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:right:width:carriageway" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:left:offset" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="parking:lane:right:offset" constraints="0" notnull_strength="0" exp_strength="0"/>
    <constraint unique_strength="0" field="error_output" constraints="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="highway" exp="" desc=""/>
    <constraint field="name" exp="" desc=""/>
    <constraint field="surface" exp="" desc=""/>
    <constraint field="parking:lane:left" exp="" desc=""/>
    <constraint field="parking:lane:right" exp="" desc=""/>
    <constraint field="width_proc" exp="" desc=""/>
    <constraint field="width_proc:effective" exp="" desc=""/>
    <constraint field="parking:lane:left:position" exp="" desc=""/>
    <constraint field="parking:lane:right:position" exp="" desc=""/>
    <constraint field="parking:lane:left:width" exp="" desc=""/>
    <constraint field="parking:lane:right:width" exp="" desc=""/>
    <constraint field="parking:lane:left:width:carriageway" exp="" desc=""/>
    <constraint field="parking:lane:right:width:carriageway" exp="" desc=""/>
    <constraint field="parking:lane:left:offset" exp="" desc=""/>
    <constraint field="parking:lane:right:offset" exp="" desc=""/>
    <constraint field="error_output" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="0" type="field" name="id" width="-1"/>
      <column hidden="0" type="field" name="highway" width="-1"/>
      <column hidden="0" type="field" name="name" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
      <column hidden="0" type="field" name="width_proc" width="-1"/>
      <column hidden="0" type="field" name="surface" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:left" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:right" width="-1"/>
      <column hidden="0" type="field" name="width_proc:effective" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:left:position" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:right:position" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:left:width" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:right:width" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:left:width:carriageway" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:right:width:carriageway" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:left:offset" width="-1"/>
      <column hidden="0" type="field" name="parking:lane:right:offset" width="-1"/>
      <column hidden="0" type="field" name="error_output" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="error_output"/>
    <field editable="1" name="highway"/>
    <field editable="1" name="id"/>
    <field editable="1" name="name"/>
    <field editable="1" name="parking:lane:left"/>
    <field editable="1" name="parking:lane:left:offset"/>
    <field editable="1" name="parking:lane:left:position"/>
    <field editable="1" name="parking:lane:left:width"/>
    <field editable="1" name="parking:lane:left:width:carriageway"/>
    <field editable="1" name="parking:lane:right"/>
    <field editable="1" name="parking:lane:right:offset"/>
    <field editable="1" name="parking:lane:right:position"/>
    <field editable="1" name="parking:lane:right:width"/>
    <field editable="1" name="parking:lane:right:width:carriageway"/>
    <field editable="1" name="processing_width"/>
    <field editable="1" name="surface"/>
    <field editable="1" name="width"/>
    <field editable="1" name="width:carriageway"/>
    <field editable="1" name="width_proc"/>
    <field editable="1" name="width_proc:effective"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="error_output"/>
    <field labelOnTop="0" name="highway"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="name"/>
    <field labelOnTop="0" name="parking:lane:left"/>
    <field labelOnTop="0" name="parking:lane:left:offset"/>
    <field labelOnTop="0" name="parking:lane:left:position"/>
    <field labelOnTop="0" name="parking:lane:left:width"/>
    <field labelOnTop="0" name="parking:lane:left:width:carriageway"/>
    <field labelOnTop="0" name="parking:lane:right"/>
    <field labelOnTop="0" name="parking:lane:right:offset"/>
    <field labelOnTop="0" name="parking:lane:right:position"/>
    <field labelOnTop="0" name="parking:lane:right:width"/>
    <field labelOnTop="0" name="parking:lane:right:width:carriageway"/>
    <field labelOnTop="0" name="processing_width"/>
    <field labelOnTop="0" name="surface"/>
    <field labelOnTop="0" name="width"/>
    <field labelOnTop="0" name="width:carriageway"/>
    <field labelOnTop="0" name="width_proc"/>
    <field labelOnTop="0" name="width_proc:effective"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
