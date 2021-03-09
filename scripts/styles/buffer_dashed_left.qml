<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" hasScaleBasedVisibilityFlag="0" readOnly="0" simplifyAlgorithm="0" version="3.14.1-Pi" maxScale="0" simplifyDrawingHints="1" simplifyMaxScale="1" styleCategories="AllStyleCategories" minScale="100000000" simplifyDrawingTol="1" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal endField="" durationField="" startField="" endExpression="" enabled="0" durationUnit="min" startExpression="" fixedDuration="0" accumulate="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" forceraster="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" force_rhr="0" name="0" clip_to_extent="1" type="fill">
        <layer enabled="1" pass="0" locked="0" class="SimpleFill">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="dot" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="no" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" pass="0" locked="0" class="CentroidFill">
          <prop v="0" k="clip_on_current_part_only"/>
          <prop v="0" k="clip_points"/>
          <prop v="1" k="point_on_all_parts"/>
          <prop v="0" k="point_on_surface"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" force_rhr="0" name="@0@1" clip_to_extent="1" type="marker">
            <layer enabled="1" pass="0" locked="0" class="SimpleMarker">
              <prop v="0" k="angle"/>
              <prop v="0,0,0,0" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="arrow" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="3" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="RenderMetersInMapUnits" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="angle" type="Map">
                      <Option name="active" value="true" type="bool"/>
                      <Option name="expression" value="&quot;angle&quot; - 90" type="QString"/>
                      <Option name="type" value="3" type="int"/>
                    </Option>
                  </Option>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory scaleBasedVisibility="0" width="15" sizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" spacingUnitScale="3x:0,0,0,0,0,0" barWidth="5" spacing="5" showAxis="1" lineSizeType="MM" height="15" sizeType="MM" penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" labelPlacementMethod="XHeight" minScaleDenominator="0" minimumSize="0" spacingUnit="MM" scaleDependency="Area" backgroundColor="#ffffff" enabled="0" penAlpha="255" maxScaleDenominator="1e+8" diagramOrientation="Up" opacity="1" direction="0" penColor="#000000" rotationOffset="270">
      <fontProperties description="Cantarell,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol alpha="1" force_rhr="0" name="" clip_to_extent="1" type="line">
          <layer enabled="1" pass="0" locked="0" class="SimpleLine">
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
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" showAll="1" placement="1" priority="0" linePlacementFlags="18" zIndex="0" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" value="0" type="double"/>
        <Option name="allowedGapsEnabled" value="false" type="bool"/>
        <Option name="allowedGapsLayer" value="" type="QString"/>
      </Option>
    </checkConfiguration>
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
    <field name="@id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="area">
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
    <field name="lit">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="noname">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="note">
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
    <field name="access">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="leisure">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="toilets:wheelchair">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="wheelchair">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cycleway:both">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lane_markings">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lanes">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxspeed">
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
    <field name="name:etymology:wikidata">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="name:etymology:wikipedia">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:left">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right">
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
    <field name="parking:lane:left:parallel">
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
    <field name="parking:lane:right:diagonal">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="postal_code">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sidewalk">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="oneway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:both">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:both">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:both:parallel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lit_by_gaslight">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="smoothness">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width:carriageway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sidewalk:both:surface">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="wikidata">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="wikipedia">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="source:maxspeed">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:default">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:time_interval">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:parallel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cycleway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="oneway:bicycle">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="bicycle">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cycleway:left">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cycleway:right">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="service">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxheight">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="turn:lanes">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:perpendicular">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:diagonal">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxweight">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:perpendicular">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tunnel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:left:capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:lane:right:capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="covered">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="layer">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="change:lanes:backward">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="change:lanes:forward">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lanes:backward">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lanes:forward">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="turn:lanes:backward">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="incline">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:both:default">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:both:time_interval">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:2:maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:right:2:time_interval">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:left:maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:left:default">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking:condition:left:time_interval">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="description">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="old_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hgv">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crossing">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crossing:kerb_extension">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="mapillary">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="survey:date">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tactile_paving">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crossing:island">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="button_operated">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="kerb">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="traffic_signals:sound">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="traffic_signals:vibration">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxwidth">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crossing:buffer_marking">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="traffic_signals:direction">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crossing_ref">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="traffic_calming:right">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="image">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="angle">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="path">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" name="" index="0"/>
    <alias field="@id" name="" index="1"/>
    <alias field="area" name="" index="2"/>
    <alias field="highway" name="" index="3"/>
    <alias field="lit" name="" index="4"/>
    <alias field="noname" name="" index="5"/>
    <alias field="note" name="" index="6"/>
    <alias field="surface" name="" index="7"/>
    <alias field="access" name="" index="8"/>
    <alias field="leisure" name="" index="9"/>
    <alias field="toilets:wheelchair" name="" index="10"/>
    <alias field="wheelchair" name="" index="11"/>
    <alias field="cycleway:both" name="" index="12"/>
    <alias field="lane_markings" name="" index="13"/>
    <alias field="lanes" name="" index="14"/>
    <alias field="maxspeed" name="" index="15"/>
    <alias field="name" name="" index="16"/>
    <alias field="name:etymology:wikidata" name="" index="17"/>
    <alias field="name:etymology:wikipedia" name="" index="18"/>
    <alias field="parking:condition:left" name="" index="19"/>
    <alias field="parking:condition:right" name="" index="20"/>
    <alias field="parking:lane:left" name="" index="21"/>
    <alias field="parking:lane:left:parallel" name="" index="22"/>
    <alias field="parking:lane:right" name="" index="23"/>
    <alias field="parking:lane:right:diagonal" name="" index="24"/>
    <alias field="postal_code" name="" index="25"/>
    <alias field="sidewalk" name="" index="26"/>
    <alias field="oneway" name="" index="27"/>
    <alias field="parking:condition:both" name="" index="28"/>
    <alias field="parking:lane:both" name="" index="29"/>
    <alias field="parking:lane:both:parallel" name="" index="30"/>
    <alias field="lit_by_gaslight" name="" index="31"/>
    <alias field="smoothness" name="" index="32"/>
    <alias field="width:carriageway" name="" index="33"/>
    <alias field="sidewalk:both:surface" name="" index="34"/>
    <alias field="wikidata" name="" index="35"/>
    <alias field="wikipedia" name="" index="36"/>
    <alias field="source:maxspeed" name="" index="37"/>
    <alias field="parking:condition:right:default" name="" index="38"/>
    <alias field="parking:condition:right:maxstay" name="" index="39"/>
    <alias field="parking:condition:right:time_interval" name="" index="40"/>
    <alias field="parking:lane:right:parallel" name="" index="41"/>
    <alias field="cycleway" name="" index="42"/>
    <alias field="oneway:bicycle" name="" index="43"/>
    <alias field="bicycle" name="" index="44"/>
    <alias field="cycleway:left" name="" index="45"/>
    <alias field="cycleway:right" name="" index="46"/>
    <alias field="service" name="" index="47"/>
    <alias field="maxheight" name="" index="48"/>
    <alias field="turn:lanes" name="" index="49"/>
    <alias field="parking:lane:left:perpendicular" name="" index="50"/>
    <alias field="parking:lane:left:diagonal" name="" index="51"/>
    <alias field="maxweight" name="" index="52"/>
    <alias field="parking:lane:right:perpendicular" name="" index="53"/>
    <alias field="tunnel" name="" index="54"/>
    <alias field="parking:lane:left:capacity" name="" index="55"/>
    <alias field="parking:lane:right:capacity" name="" index="56"/>
    <alias field="covered" name="" index="57"/>
    <alias field="layer" name="" index="58"/>
    <alias field="change:lanes:backward" name="" index="59"/>
    <alias field="change:lanes:forward" name="" index="60"/>
    <alias field="lanes:backward" name="" index="61"/>
    <alias field="lanes:forward" name="" index="62"/>
    <alias field="turn:lanes:backward" name="" index="63"/>
    <alias field="incline" name="" index="64"/>
    <alias field="parking:condition:both:default" name="" index="65"/>
    <alias field="parking:condition:both:time_interval" name="" index="66"/>
    <alias field="parking:condition:right:2" name="" index="67"/>
    <alias field="parking:condition:right:2:maxstay" name="" index="68"/>
    <alias field="parking:condition:right:2:time_interval" name="" index="69"/>
    <alias field="parking:condition:left:maxstay" name="" index="70"/>
    <alias field="parking:condition:left:default" name="" index="71"/>
    <alias field="parking:condition:left:time_interval" name="" index="72"/>
    <alias field="description" name="" index="73"/>
    <alias field="old_name" name="" index="74"/>
    <alias field="hgv" name="" index="75"/>
    <alias field="crossing" name="" index="76"/>
    <alias field="crossing:kerb_extension" name="" index="77"/>
    <alias field="mapillary" name="" index="78"/>
    <alias field="survey:date" name="" index="79"/>
    <alias field="tactile_paving" name="" index="80"/>
    <alias field="crossing:island" name="" index="81"/>
    <alias field="button_operated" name="" index="82"/>
    <alias field="kerb" name="" index="83"/>
    <alias field="traffic_signals:sound" name="" index="84"/>
    <alias field="traffic_signals:vibration" name="" index="85"/>
    <alias field="maxwidth" name="" index="86"/>
    <alias field="crossing:buffer_marking" name="" index="87"/>
    <alias field="traffic_signals:direction" name="" index="88"/>
    <alias field="crossing_ref" name="" index="89"/>
    <alias field="traffic_calming:right" name="" index="90"/>
    <alias field="image" name="" index="91"/>
    <alias field="angle" name="" index="92"/>
    <alias field="path" name="" index="93"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="@id" applyOnUpdate="0" expression=""/>
    <default field="area" applyOnUpdate="0" expression=""/>
    <default field="highway" applyOnUpdate="0" expression=""/>
    <default field="lit" applyOnUpdate="0" expression=""/>
    <default field="noname" applyOnUpdate="0" expression=""/>
    <default field="note" applyOnUpdate="0" expression=""/>
    <default field="surface" applyOnUpdate="0" expression=""/>
    <default field="access" applyOnUpdate="0" expression=""/>
    <default field="leisure" applyOnUpdate="0" expression=""/>
    <default field="toilets:wheelchair" applyOnUpdate="0" expression=""/>
    <default field="wheelchair" applyOnUpdate="0" expression=""/>
    <default field="cycleway:both" applyOnUpdate="0" expression=""/>
    <default field="lane_markings" applyOnUpdate="0" expression=""/>
    <default field="lanes" applyOnUpdate="0" expression=""/>
    <default field="maxspeed" applyOnUpdate="0" expression=""/>
    <default field="name" applyOnUpdate="0" expression=""/>
    <default field="name:etymology:wikidata" applyOnUpdate="0" expression=""/>
    <default field="name:etymology:wikipedia" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:left" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:parallel" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:diagonal" applyOnUpdate="0" expression=""/>
    <default field="postal_code" applyOnUpdate="0" expression=""/>
    <default field="sidewalk" applyOnUpdate="0" expression=""/>
    <default field="oneway" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:both" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:both" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:both:parallel" applyOnUpdate="0" expression=""/>
    <default field="lit_by_gaslight" applyOnUpdate="0" expression=""/>
    <default field="smoothness" applyOnUpdate="0" expression=""/>
    <default field="width:carriageway" applyOnUpdate="0" expression=""/>
    <default field="sidewalk:both:surface" applyOnUpdate="0" expression=""/>
    <default field="wikidata" applyOnUpdate="0" expression=""/>
    <default field="wikipedia" applyOnUpdate="0" expression=""/>
    <default field="source:maxspeed" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:default" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:maxstay" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:time_interval" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:parallel" applyOnUpdate="0" expression=""/>
    <default field="cycleway" applyOnUpdate="0" expression=""/>
    <default field="oneway:bicycle" applyOnUpdate="0" expression=""/>
    <default field="bicycle" applyOnUpdate="0" expression=""/>
    <default field="cycleway:left" applyOnUpdate="0" expression=""/>
    <default field="cycleway:right" applyOnUpdate="0" expression=""/>
    <default field="service" applyOnUpdate="0" expression=""/>
    <default field="maxheight" applyOnUpdate="0" expression=""/>
    <default field="turn:lanes" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:perpendicular" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:diagonal" applyOnUpdate="0" expression=""/>
    <default field="maxweight" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:perpendicular" applyOnUpdate="0" expression=""/>
    <default field="tunnel" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:capacity" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:capacity" applyOnUpdate="0" expression=""/>
    <default field="covered" applyOnUpdate="0" expression=""/>
    <default field="layer" applyOnUpdate="0" expression=""/>
    <default field="change:lanes:backward" applyOnUpdate="0" expression=""/>
    <default field="change:lanes:forward" applyOnUpdate="0" expression=""/>
    <default field="lanes:backward" applyOnUpdate="0" expression=""/>
    <default field="lanes:forward" applyOnUpdate="0" expression=""/>
    <default field="turn:lanes:backward" applyOnUpdate="0" expression=""/>
    <default field="incline" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:both:default" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:both:time_interval" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:2" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:2:maxstay" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:right:2:time_interval" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:left:maxstay" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:left:default" applyOnUpdate="0" expression=""/>
    <default field="parking:condition:left:time_interval" applyOnUpdate="0" expression=""/>
    <default field="description" applyOnUpdate="0" expression=""/>
    <default field="old_name" applyOnUpdate="0" expression=""/>
    <default field="hgv" applyOnUpdate="0" expression=""/>
    <default field="crossing" applyOnUpdate="0" expression=""/>
    <default field="crossing:kerb_extension" applyOnUpdate="0" expression=""/>
    <default field="mapillary" applyOnUpdate="0" expression=""/>
    <default field="survey:date" applyOnUpdate="0" expression=""/>
    <default field="tactile_paving" applyOnUpdate="0" expression=""/>
    <default field="crossing:island" applyOnUpdate="0" expression=""/>
    <default field="button_operated" applyOnUpdate="0" expression=""/>
    <default field="kerb" applyOnUpdate="0" expression=""/>
    <default field="traffic_signals:sound" applyOnUpdate="0" expression=""/>
    <default field="traffic_signals:vibration" applyOnUpdate="0" expression=""/>
    <default field="maxwidth" applyOnUpdate="0" expression=""/>
    <default field="crossing:buffer_marking" applyOnUpdate="0" expression=""/>
    <default field="traffic_signals:direction" applyOnUpdate="0" expression=""/>
    <default field="crossing_ref" applyOnUpdate="0" expression=""/>
    <default field="traffic_calming:right" applyOnUpdate="0" expression=""/>
    <default field="image" applyOnUpdate="0" expression=""/>
    <default field="angle" applyOnUpdate="0" expression=""/>
    <default field="path" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="id" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="@id" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="area" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="highway" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lit" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="noname" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="note" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="surface" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="access" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="leisure" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="toilets:wheelchair" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="wheelchair" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="cycleway:both" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lane_markings" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lanes" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="maxspeed" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="name" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="name:etymology:wikidata" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="name:etymology:wikipedia" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:left" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:left" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:left:parallel" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:right" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:right:diagonal" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="postal_code" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="sidewalk" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="oneway" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:both" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:both" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:both:parallel" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lit_by_gaslight" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="smoothness" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="width:carriageway" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="sidewalk:both:surface" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="wikidata" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="wikipedia" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="source:maxspeed" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:default" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:maxstay" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:time_interval" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:right:parallel" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="cycleway" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="oneway:bicycle" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="bicycle" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="cycleway:left" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="cycleway:right" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="service" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="maxheight" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="turn:lanes" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:left:perpendicular" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:left:diagonal" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="maxweight" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:right:perpendicular" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="tunnel" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:left:capacity" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:lane:right:capacity" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="covered" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="layer" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="change:lanes:backward" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="change:lanes:forward" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lanes:backward" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="lanes:forward" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="turn:lanes:backward" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="incline" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:both:default" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:both:time_interval" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:2" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:2:maxstay" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:right:2:time_interval" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:left:maxstay" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:left:default" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="parking:condition:left:time_interval" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="description" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="old_name" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="hgv" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="crossing" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="crossing:kerb_extension" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="mapillary" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="survey:date" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="tactile_paving" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="crossing:island" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="button_operated" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="kerb" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="traffic_signals:sound" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="traffic_signals:vibration" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="maxwidth" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="crossing:buffer_marking" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="traffic_signals:direction" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="crossing_ref" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="traffic_calming:right" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="image" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="angle" unique_strength="0" exp_strength="0" constraints="0"/>
    <constraint notnull_strength="0" field="path" unique_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="@id" desc="" exp=""/>
    <constraint field="area" desc="" exp=""/>
    <constraint field="highway" desc="" exp=""/>
    <constraint field="lit" desc="" exp=""/>
    <constraint field="noname" desc="" exp=""/>
    <constraint field="note" desc="" exp=""/>
    <constraint field="surface" desc="" exp=""/>
    <constraint field="access" desc="" exp=""/>
    <constraint field="leisure" desc="" exp=""/>
    <constraint field="toilets:wheelchair" desc="" exp=""/>
    <constraint field="wheelchair" desc="" exp=""/>
    <constraint field="cycleway:both" desc="" exp=""/>
    <constraint field="lane_markings" desc="" exp=""/>
    <constraint field="lanes" desc="" exp=""/>
    <constraint field="maxspeed" desc="" exp=""/>
    <constraint field="name" desc="" exp=""/>
    <constraint field="name:etymology:wikidata" desc="" exp=""/>
    <constraint field="name:etymology:wikipedia" desc="" exp=""/>
    <constraint field="parking:condition:left" desc="" exp=""/>
    <constraint field="parking:condition:right" desc="" exp=""/>
    <constraint field="parking:lane:left" desc="" exp=""/>
    <constraint field="parking:lane:left:parallel" desc="" exp=""/>
    <constraint field="parking:lane:right" desc="" exp=""/>
    <constraint field="parking:lane:right:diagonal" desc="" exp=""/>
    <constraint field="postal_code" desc="" exp=""/>
    <constraint field="sidewalk" desc="" exp=""/>
    <constraint field="oneway" desc="" exp=""/>
    <constraint field="parking:condition:both" desc="" exp=""/>
    <constraint field="parking:lane:both" desc="" exp=""/>
    <constraint field="parking:lane:both:parallel" desc="" exp=""/>
    <constraint field="lit_by_gaslight" desc="" exp=""/>
    <constraint field="smoothness" desc="" exp=""/>
    <constraint field="width:carriageway" desc="" exp=""/>
    <constraint field="sidewalk:both:surface" desc="" exp=""/>
    <constraint field="wikidata" desc="" exp=""/>
    <constraint field="wikipedia" desc="" exp=""/>
    <constraint field="source:maxspeed" desc="" exp=""/>
    <constraint field="parking:condition:right:default" desc="" exp=""/>
    <constraint field="parking:condition:right:maxstay" desc="" exp=""/>
    <constraint field="parking:condition:right:time_interval" desc="" exp=""/>
    <constraint field="parking:lane:right:parallel" desc="" exp=""/>
    <constraint field="cycleway" desc="" exp=""/>
    <constraint field="oneway:bicycle" desc="" exp=""/>
    <constraint field="bicycle" desc="" exp=""/>
    <constraint field="cycleway:left" desc="" exp=""/>
    <constraint field="cycleway:right" desc="" exp=""/>
    <constraint field="service" desc="" exp=""/>
    <constraint field="maxheight" desc="" exp=""/>
    <constraint field="turn:lanes" desc="" exp=""/>
    <constraint field="parking:lane:left:perpendicular" desc="" exp=""/>
    <constraint field="parking:lane:left:diagonal" desc="" exp=""/>
    <constraint field="maxweight" desc="" exp=""/>
    <constraint field="parking:lane:right:perpendicular" desc="" exp=""/>
    <constraint field="tunnel" desc="" exp=""/>
    <constraint field="parking:lane:left:capacity" desc="" exp=""/>
    <constraint field="parking:lane:right:capacity" desc="" exp=""/>
    <constraint field="covered" desc="" exp=""/>
    <constraint field="layer" desc="" exp=""/>
    <constraint field="change:lanes:backward" desc="" exp=""/>
    <constraint field="change:lanes:forward" desc="" exp=""/>
    <constraint field="lanes:backward" desc="" exp=""/>
    <constraint field="lanes:forward" desc="" exp=""/>
    <constraint field="turn:lanes:backward" desc="" exp=""/>
    <constraint field="incline" desc="" exp=""/>
    <constraint field="parking:condition:both:default" desc="" exp=""/>
    <constraint field="parking:condition:both:time_interval" desc="" exp=""/>
    <constraint field="parking:condition:right:2" desc="" exp=""/>
    <constraint field="parking:condition:right:2:maxstay" desc="" exp=""/>
    <constraint field="parking:condition:right:2:time_interval" desc="" exp=""/>
    <constraint field="parking:condition:left:maxstay" desc="" exp=""/>
    <constraint field="parking:condition:left:default" desc="" exp=""/>
    <constraint field="parking:condition:left:time_interval" desc="" exp=""/>
    <constraint field="description" desc="" exp=""/>
    <constraint field="old_name" desc="" exp=""/>
    <constraint field="hgv" desc="" exp=""/>
    <constraint field="crossing" desc="" exp=""/>
    <constraint field="crossing:kerb_extension" desc="" exp=""/>
    <constraint field="mapillary" desc="" exp=""/>
    <constraint field="survey:date" desc="" exp=""/>
    <constraint field="tactile_paving" desc="" exp=""/>
    <constraint field="crossing:island" desc="" exp=""/>
    <constraint field="button_operated" desc="" exp=""/>
    <constraint field="kerb" desc="" exp=""/>
    <constraint field="traffic_signals:sound" desc="" exp=""/>
    <constraint field="traffic_signals:vibration" desc="" exp=""/>
    <constraint field="maxwidth" desc="" exp=""/>
    <constraint field="crossing:buffer_marking" desc="" exp=""/>
    <constraint field="traffic_signals:direction" desc="" exp=""/>
    <constraint field="crossing_ref" desc="" exp=""/>
    <constraint field="traffic_calming:right" desc="" exp=""/>
    <constraint field="image" desc="" exp=""/>
    <constraint field="angle" desc="" exp=""/>
    <constraint field="path" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="id" width="-1" type="field" hidden="0"/>
      <column name="highway" width="-1" type="field" hidden="0"/>
      <column name="name" width="-1" type="field" hidden="0"/>
      <column name="surface" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:left" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:right" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
      <column name="@id" width="-1" type="field" hidden="0"/>
      <column name="area" width="-1" type="field" hidden="0"/>
      <column name="lit" width="-1" type="field" hidden="0"/>
      <column name="noname" width="-1" type="field" hidden="0"/>
      <column name="note" width="-1" type="field" hidden="0"/>
      <column name="access" width="-1" type="field" hidden="0"/>
      <column name="leisure" width="-1" type="field" hidden="0"/>
      <column name="toilets:wheelchair" width="-1" type="field" hidden="0"/>
      <column name="wheelchair" width="-1" type="field" hidden="0"/>
      <column name="cycleway:both" width="-1" type="field" hidden="0"/>
      <column name="lane_markings" width="-1" type="field" hidden="0"/>
      <column name="lanes" width="-1" type="field" hidden="0"/>
      <column name="maxspeed" width="-1" type="field" hidden="0"/>
      <column name="name:etymology:wikidata" width="-1" type="field" hidden="0"/>
      <column name="name:etymology:wikipedia" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:left" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:left:parallel" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:right:diagonal" width="-1" type="field" hidden="0"/>
      <column name="postal_code" width="-1" type="field" hidden="0"/>
      <column name="sidewalk" width="-1" type="field" hidden="0"/>
      <column name="oneway" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:both" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:both" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:both:parallel" width="-1" type="field" hidden="0"/>
      <column name="lit_by_gaslight" width="-1" type="field" hidden="0"/>
      <column name="smoothness" width="-1" type="field" hidden="0"/>
      <column name="width:carriageway" width="-1" type="field" hidden="0"/>
      <column name="sidewalk:both:surface" width="-1" type="field" hidden="0"/>
      <column name="wikidata" width="-1" type="field" hidden="0"/>
      <column name="wikipedia" width="-1" type="field" hidden="0"/>
      <column name="source:maxspeed" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:default" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:maxstay" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:time_interval" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:right:parallel" width="-1" type="field" hidden="0"/>
      <column name="cycleway" width="-1" type="field" hidden="0"/>
      <column name="oneway:bicycle" width="-1" type="field" hidden="0"/>
      <column name="bicycle" width="-1" type="field" hidden="0"/>
      <column name="cycleway:left" width="-1" type="field" hidden="0"/>
      <column name="cycleway:right" width="-1" type="field" hidden="0"/>
      <column name="service" width="-1" type="field" hidden="0"/>
      <column name="maxheight" width="-1" type="field" hidden="0"/>
      <column name="turn:lanes" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:left:perpendicular" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:left:diagonal" width="-1" type="field" hidden="0"/>
      <column name="maxweight" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:right:perpendicular" width="-1" type="field" hidden="0"/>
      <column name="tunnel" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:left:capacity" width="-1" type="field" hidden="0"/>
      <column name="parking:lane:right:capacity" width="-1" type="field" hidden="0"/>
      <column name="covered" width="-1" type="field" hidden="0"/>
      <column name="layer" width="-1" type="field" hidden="0"/>
      <column name="change:lanes:backward" width="-1" type="field" hidden="0"/>
      <column name="change:lanes:forward" width="-1" type="field" hidden="0"/>
      <column name="lanes:backward" width="-1" type="field" hidden="0"/>
      <column name="lanes:forward" width="-1" type="field" hidden="0"/>
      <column name="turn:lanes:backward" width="-1" type="field" hidden="0"/>
      <column name="incline" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:both:default" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:both:time_interval" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:2" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:2:maxstay" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:right:2:time_interval" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:left:maxstay" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:left:default" width="-1" type="field" hidden="0"/>
      <column name="parking:condition:left:time_interval" width="-1" type="field" hidden="0"/>
      <column name="description" width="-1" type="field" hidden="0"/>
      <column name="old_name" width="-1" type="field" hidden="0"/>
      <column name="hgv" width="-1" type="field" hidden="0"/>
      <column name="crossing" width="-1" type="field" hidden="0"/>
      <column name="crossing:kerb_extension" width="-1" type="field" hidden="0"/>
      <column name="mapillary" width="-1" type="field" hidden="0"/>
      <column name="survey:date" width="-1" type="field" hidden="0"/>
      <column name="tactile_paving" width="-1" type="field" hidden="0"/>
      <column name="crossing:island" width="-1" type="field" hidden="0"/>
      <column name="button_operated" width="-1" type="field" hidden="0"/>
      <column name="kerb" width="-1" type="field" hidden="0"/>
      <column name="traffic_signals:sound" width="-1" type="field" hidden="0"/>
      <column name="traffic_signals:vibration" width="-1" type="field" hidden="0"/>
      <column name="maxwidth" width="-1" type="field" hidden="0"/>
      <column name="crossing:buffer_marking" width="-1" type="field" hidden="0"/>
      <column name="traffic_signals:direction" width="-1" type="field" hidden="0"/>
      <column name="crossing_ref" width="-1" type="field" hidden="0"/>
      <column name="traffic_calming:right" width="-1" type="field" hidden="0"/>
      <column name="image" width="-1" type="field" hidden="0"/>
      <column name="angle" width="-1" type="field" hidden="0"/>
      <column name="path" width="-1" type="field" hidden="0"/>
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
    <field name="@id" editable="1"/>
    <field name="access" editable="1"/>
    <field name="angle" editable="1"/>
    <field name="area" editable="1"/>
    <field name="bicycle" editable="1"/>
    <field name="button_operated" editable="1"/>
    <field name="capacity" editable="1"/>
    <field name="change:lanes:backward" editable="1"/>
    <field name="change:lanes:forward" editable="1"/>
    <field name="condition" editable="1"/>
    <field name="condition:other" editable="1"/>
    <field name="condition:other:time" editable="1"/>
    <field name="covered" editable="1"/>
    <field name="crossing" editable="1"/>
    <field name="crossing:buffer_marking" editable="1"/>
    <field name="crossing:island" editable="1"/>
    <field name="crossing:kerb_extension" editable="1"/>
    <field name="crossing_ref" editable="1"/>
    <field name="cycleway" editable="1"/>
    <field name="cycleway:both" editable="1"/>
    <field name="cycleway:left" editable="1"/>
    <field name="cycleway:right" editable="1"/>
    <field name="description" editable="1"/>
    <field name="error_output" editable="1"/>
    <field name="error_output_2" editable="1"/>
    <field name="hgv" editable="1"/>
    <field name="highway" editable="1"/>
    <field name="highway:name" editable="1"/>
    <field name="highway:width_proc" editable="1"/>
    <field name="highway:width_proc:effective" editable="1"/>
    <field name="highway_2" editable="1"/>
    <field name="id" editable="1"/>
    <field name="id_2" editable="1"/>
    <field name="image" editable="1"/>
    <field name="incline" editable="1"/>
    <field name="kerb" editable="1"/>
    <field name="lane_markings" editable="1"/>
    <field name="lanes" editable="1"/>
    <field name="lanes:backward" editable="1"/>
    <field name="lanes:forward" editable="1"/>
    <field name="layer" editable="1"/>
    <field name="leisure" editable="1"/>
    <field name="lit" editable="1"/>
    <field name="lit_by_gaslight" editable="1"/>
    <field name="mapillary" editable="1"/>
    <field name="maxheight" editable="1"/>
    <field name="maxspeed" editable="1"/>
    <field name="maxstay" editable="1"/>
    <field name="maxweight" editable="1"/>
    <field name="maxwidth" editable="1"/>
    <field name="name" editable="1"/>
    <field name="name:etymology:wikidata" editable="1"/>
    <field name="name:etymology:wikipedia" editable="1"/>
    <field name="noname" editable="1"/>
    <field name="note" editable="1"/>
    <field name="offset" editable="1"/>
    <field name="old_name" editable="1"/>
    <field name="oneway" editable="1"/>
    <field name="oneway:bicycle" editable="1"/>
    <field name="parking" editable="1"/>
    <field name="parking:condition:both" editable="1"/>
    <field name="parking:condition:both:default" editable="1"/>
    <field name="parking:condition:both:time_interval" editable="1"/>
    <field name="parking:condition:left" editable="1"/>
    <field name="parking:condition:left:default" editable="1"/>
    <field name="parking:condition:left:maxstay" editable="1"/>
    <field name="parking:condition:left:time_interval" editable="1"/>
    <field name="parking:condition:right" editable="1"/>
    <field name="parking:condition:right:2" editable="1"/>
    <field name="parking:condition:right:2:maxstay" editable="1"/>
    <field name="parking:condition:right:2:time_interval" editable="1"/>
    <field name="parking:condition:right:default" editable="1"/>
    <field name="parking:condition:right:maxstay" editable="1"/>
    <field name="parking:condition:right:time_interval" editable="1"/>
    <field name="parking:lane:both" editable="1"/>
    <field name="parking:lane:both:parallel" editable="1"/>
    <field name="parking:lane:left" editable="1"/>
    <field name="parking:lane:left:capacity" editable="1"/>
    <field name="parking:lane:left:diagonal" editable="1"/>
    <field name="parking:lane:left:offset" editable="1"/>
    <field name="parking:lane:left:parallel" editable="1"/>
    <field name="parking:lane:left:perpendicular" editable="1"/>
    <field name="parking:lane:left:position" editable="1"/>
    <field name="parking:lane:left:width" editable="1"/>
    <field name="parking:lane:left:width:carriageway" editable="1"/>
    <field name="parking:lane:right" editable="1"/>
    <field name="parking:lane:right:capacity" editable="1"/>
    <field name="parking:lane:right:diagonal" editable="1"/>
    <field name="parking:lane:right:offset" editable="1"/>
    <field name="parking:lane:right:parallel" editable="1"/>
    <field name="parking:lane:right:perpendicular" editable="1"/>
    <field name="parking:lane:right:position" editable="1"/>
    <field name="parking:lane:right:width" editable="1"/>
    <field name="parking:lane:right:width:carriageway" editable="1"/>
    <field name="path" editable="1"/>
    <field name="position" editable="1"/>
    <field name="postal_code" editable="1"/>
    <field name="service" editable="1"/>
    <field name="sidewalk" editable="1"/>
    <field name="sidewalk:both:surface" editable="1"/>
    <field name="smoothness" editable="1"/>
    <field name="source:maxspeed" editable="1"/>
    <field name="surface" editable="1"/>
    <field name="survey:date" editable="1"/>
    <field name="tactile_paving" editable="1"/>
    <field name="toilets:wheelchair" editable="1"/>
    <field name="traffic_calming:right" editable="1"/>
    <field name="traffic_signals:direction" editable="1"/>
    <field name="traffic_signals:sound" editable="1"/>
    <field name="traffic_signals:vibration" editable="1"/>
    <field name="tunnel" editable="1"/>
    <field name="turn:lanes" editable="1"/>
    <field name="turn:lanes:backward" editable="1"/>
    <field name="wheelchair" editable="1"/>
    <field name="width" editable="1"/>
    <field name="width:carriageway" editable="1"/>
    <field name="width_proc" editable="1"/>
    <field name="width_proc:effective" editable="1"/>
    <field name="wikidata" editable="1"/>
    <field name="wikipedia" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="@id" labelOnTop="0"/>
    <field name="access" labelOnTop="0"/>
    <field name="angle" labelOnTop="0"/>
    <field name="area" labelOnTop="0"/>
    <field name="bicycle" labelOnTop="0"/>
    <field name="button_operated" labelOnTop="0"/>
    <field name="capacity" labelOnTop="0"/>
    <field name="change:lanes:backward" labelOnTop="0"/>
    <field name="change:lanes:forward" labelOnTop="0"/>
    <field name="condition" labelOnTop="0"/>
    <field name="condition:other" labelOnTop="0"/>
    <field name="condition:other:time" labelOnTop="0"/>
    <field name="covered" labelOnTop="0"/>
    <field name="crossing" labelOnTop="0"/>
    <field name="crossing:buffer_marking" labelOnTop="0"/>
    <field name="crossing:island" labelOnTop="0"/>
    <field name="crossing:kerb_extension" labelOnTop="0"/>
    <field name="crossing_ref" labelOnTop="0"/>
    <field name="cycleway" labelOnTop="0"/>
    <field name="cycleway:both" labelOnTop="0"/>
    <field name="cycleway:left" labelOnTop="0"/>
    <field name="cycleway:right" labelOnTop="0"/>
    <field name="description" labelOnTop="0"/>
    <field name="error_output" labelOnTop="0"/>
    <field name="error_output_2" labelOnTop="0"/>
    <field name="hgv" labelOnTop="0"/>
    <field name="highway" labelOnTop="0"/>
    <field name="highway:name" labelOnTop="0"/>
    <field name="highway:width_proc" labelOnTop="0"/>
    <field name="highway:width_proc:effective" labelOnTop="0"/>
    <field name="highway_2" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="id_2" labelOnTop="0"/>
    <field name="image" labelOnTop="0"/>
    <field name="incline" labelOnTop="0"/>
    <field name="kerb" labelOnTop="0"/>
    <field name="lane_markings" labelOnTop="0"/>
    <field name="lanes" labelOnTop="0"/>
    <field name="lanes:backward" labelOnTop="0"/>
    <field name="lanes:forward" labelOnTop="0"/>
    <field name="layer" labelOnTop="0"/>
    <field name="leisure" labelOnTop="0"/>
    <field name="lit" labelOnTop="0"/>
    <field name="lit_by_gaslight" labelOnTop="0"/>
    <field name="mapillary" labelOnTop="0"/>
    <field name="maxheight" labelOnTop="0"/>
    <field name="maxspeed" labelOnTop="0"/>
    <field name="maxstay" labelOnTop="0"/>
    <field name="maxweight" labelOnTop="0"/>
    <field name="maxwidth" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="name:etymology:wikidata" labelOnTop="0"/>
    <field name="name:etymology:wikipedia" labelOnTop="0"/>
    <field name="noname" labelOnTop="0"/>
    <field name="note" labelOnTop="0"/>
    <field name="offset" labelOnTop="0"/>
    <field name="old_name" labelOnTop="0"/>
    <field name="oneway" labelOnTop="0"/>
    <field name="oneway:bicycle" labelOnTop="0"/>
    <field name="parking" labelOnTop="0"/>
    <field name="parking:condition:both" labelOnTop="0"/>
    <field name="parking:condition:both:default" labelOnTop="0"/>
    <field name="parking:condition:both:time_interval" labelOnTop="0"/>
    <field name="parking:condition:left" labelOnTop="0"/>
    <field name="parking:condition:left:default" labelOnTop="0"/>
    <field name="parking:condition:left:maxstay" labelOnTop="0"/>
    <field name="parking:condition:left:time_interval" labelOnTop="0"/>
    <field name="parking:condition:right" labelOnTop="0"/>
    <field name="parking:condition:right:2" labelOnTop="0"/>
    <field name="parking:condition:right:2:maxstay" labelOnTop="0"/>
    <field name="parking:condition:right:2:time_interval" labelOnTop="0"/>
    <field name="parking:condition:right:default" labelOnTop="0"/>
    <field name="parking:condition:right:maxstay" labelOnTop="0"/>
    <field name="parking:condition:right:time_interval" labelOnTop="0"/>
    <field name="parking:lane:both" labelOnTop="0"/>
    <field name="parking:lane:both:parallel" labelOnTop="0"/>
    <field name="parking:lane:left" labelOnTop="0"/>
    <field name="parking:lane:left:capacity" labelOnTop="0"/>
    <field name="parking:lane:left:diagonal" labelOnTop="0"/>
    <field name="parking:lane:left:offset" labelOnTop="0"/>
    <field name="parking:lane:left:parallel" labelOnTop="0"/>
    <field name="parking:lane:left:perpendicular" labelOnTop="0"/>
    <field name="parking:lane:left:position" labelOnTop="0"/>
    <field name="parking:lane:left:width" labelOnTop="0"/>
    <field name="parking:lane:left:width:carriageway" labelOnTop="0"/>
    <field name="parking:lane:right" labelOnTop="0"/>
    <field name="parking:lane:right:capacity" labelOnTop="0"/>
    <field name="parking:lane:right:diagonal" labelOnTop="0"/>
    <field name="parking:lane:right:offset" labelOnTop="0"/>
    <field name="parking:lane:right:parallel" labelOnTop="0"/>
    <field name="parking:lane:right:perpendicular" labelOnTop="0"/>
    <field name="parking:lane:right:position" labelOnTop="0"/>
    <field name="parking:lane:right:width" labelOnTop="0"/>
    <field name="parking:lane:right:width:carriageway" labelOnTop="0"/>
    <field name="path" labelOnTop="0"/>
    <field name="position" labelOnTop="0"/>
    <field name="postal_code" labelOnTop="0"/>
    <field name="service" labelOnTop="0"/>
    <field name="sidewalk" labelOnTop="0"/>
    <field name="sidewalk:both:surface" labelOnTop="0"/>
    <field name="smoothness" labelOnTop="0"/>
    <field name="source:maxspeed" labelOnTop="0"/>
    <field name="surface" labelOnTop="0"/>
    <field name="survey:date" labelOnTop="0"/>
    <field name="tactile_paving" labelOnTop="0"/>
    <field name="toilets:wheelchair" labelOnTop="0"/>
    <field name="traffic_calming:right" labelOnTop="0"/>
    <field name="traffic_signals:direction" labelOnTop="0"/>
    <field name="traffic_signals:sound" labelOnTop="0"/>
    <field name="traffic_signals:vibration" labelOnTop="0"/>
    <field name="tunnel" labelOnTop="0"/>
    <field name="turn:lanes" labelOnTop="0"/>
    <field name="turn:lanes:backward" labelOnTop="0"/>
    <field name="wheelchair" labelOnTop="0"/>
    <field name="width" labelOnTop="0"/>
    <field name="width:carriageway" labelOnTop="0"/>
    <field name="width_proc" labelOnTop="0"/>
    <field name="width_proc:effective" labelOnTop="0"/>
    <field name="wikidata" labelOnTop="0"/>
    <field name="wikipedia" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"highway:name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
