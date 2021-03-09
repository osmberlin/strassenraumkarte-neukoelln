<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" readOnly="0" version="3.14.1-Pi" styleCategories="AllStyleCategories" maxScale="0" simplifyAlgorithm="0" minScale="100000000" labelsEnabled="0" simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal accumulate="0" durationUnit="min" endExpression="" durationField="" endField="" enabled="0" startExpression="" startField="" fixedDuration="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" symbollevels="0" forceraster="0" type="singleSymbol">
    <symbols>
      <symbol force_rhr="0" name="0" type="fill" clip_to_extent="1" alpha="1">
        <layer locked="0" enabled="1" pass="0" class="SimpleFill">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="dot"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory minScaleDenominator="0" labelPlacementMethod="XHeight" spacingUnit="MM" width="15" spacingUnitScale="3x:0,0,0,0,0,0" opacity="1" backgroundColor="#ffffff" penWidth="0" scaleBasedVisibility="0" height="15" direction="0" scaleDependency="Area" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" rotationOffset="270" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" penAlpha="255" diagramOrientation="Up" maxScaleDenominator="1e+8" penColor="#000000" lineSizeType="MM" showAxis="1" spacing="5" barWidth="5" minimumSize="0" enabled="0">
      <fontProperties description="Cantarell,11,-1,5,50,0,0,0,0,0" style=""/>
      <axisSymbol>
        <symbol force_rhr="0" name="" type="line" clip_to_extent="1" alpha="1">
          <layer locked="0" enabled="1" pass="0" class="SimpleLine">
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString"/>
                <Option name="properties"/>
                <Option value="collection" name="type" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" dist="0" linePlacementFlags="18" zIndex="0" obstacle="0" placement="1" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option value="0" name="allowedGapsBuffer" type="double"/>
        <Option value="false" name="allowedGapsEnabled" type="bool"/>
        <Option value="" name="allowedGapsLayer" type="QString"/>
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
    <field name="highway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc:effective">
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
    <field name="parking">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="position">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other:time">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="offset">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_2">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway_2">
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
    <field name="error_output_2">
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
    <alias field="highway:name" index="2" name=""/>
    <alias field="highway:width_proc" index="3" name=""/>
    <alias field="highway:width_proc:effective" index="4" name=""/>
    <alias field="error_output" index="5" name=""/>
    <alias field="parking" index="6" name=""/>
    <alias field="position" index="7" name=""/>
    <alias field="condition" index="8" name=""/>
    <alias field="condition:other" index="9" name=""/>
    <alias field="condition:other:time" index="10" name=""/>
    <alias field="maxstay" index="11" name=""/>
    <alias field="capacity" index="12" name=""/>
    <alias field="width" index="13" name=""/>
    <alias field="offset" index="14" name=""/>
    <alias field="id_2" index="15" name=""/>
    <alias field="highway_2" index="16" name=""/>
    <alias field="name" index="17" name=""/>
    <alias field="surface" index="18" name=""/>
    <alias field="parking:lane:left" index="19" name=""/>
    <alias field="parking:lane:right" index="20" name=""/>
    <alias field="width_proc" index="21" name=""/>
    <alias field="width_proc:effective" index="22" name=""/>
    <alias field="parking:lane:left:position" index="23" name=""/>
    <alias field="parking:lane:right:position" index="24" name=""/>
    <alias field="parking:lane:left:width" index="25" name=""/>
    <alias field="parking:lane:right:width" index="26" name=""/>
    <alias field="parking:lane:left:width:carriageway" index="27" name=""/>
    <alias field="parking:lane:right:width:carriageway" index="28" name=""/>
    <alias field="parking:lane:left:offset" index="29" name=""/>
    <alias field="parking:lane:right:offset" index="30" name=""/>
    <alias field="error_output_2" index="31" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="highway" applyOnUpdate="0" expression=""/>
    <default field="highway:name" applyOnUpdate="0" expression=""/>
    <default field="highway:width_proc" applyOnUpdate="0" expression=""/>
    <default field="highway:width_proc:effective" applyOnUpdate="0" expression=""/>
    <default field="error_output" applyOnUpdate="0" expression=""/>
    <default field="parking" applyOnUpdate="0" expression=""/>
    <default field="position" applyOnUpdate="0" expression=""/>
    <default field="condition" applyOnUpdate="0" expression=""/>
    <default field="condition:other" applyOnUpdate="0" expression=""/>
    <default field="condition:other:time" applyOnUpdate="0" expression=""/>
    <default field="maxstay" applyOnUpdate="0" expression=""/>
    <default field="capacity" applyOnUpdate="0" expression=""/>
    <default field="width" applyOnUpdate="0" expression=""/>
    <default field="offset" applyOnUpdate="0" expression=""/>
    <default field="id_2" applyOnUpdate="0" expression=""/>
    <default field="highway_2" applyOnUpdate="0" expression=""/>
    <default field="name" applyOnUpdate="0" expression=""/>
    <default field="surface" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right" applyOnUpdate="0" expression=""/>
    <default field="width_proc" applyOnUpdate="0" expression=""/>
    <default field="width_proc:effective" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:position" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:position" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:width" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:width" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:width:carriageway" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:width:carriageway" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:left:offset" applyOnUpdate="0" expression=""/>
    <default field="parking:lane:right:offset" applyOnUpdate="0" expression=""/>
    <default field="error_output_2" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="id" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="highway" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="highway:name" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="highway:width_proc" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="highway:width_proc:effective" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="error_output" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="position" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="condition" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="condition:other" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="condition:other:time" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="maxstay" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="capacity" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="width" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="offset" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="id_2" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="highway_2" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="name" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="surface" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:left" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:right" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="width_proc" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="width_proc:effective" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:left:position" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:right:position" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:left:width" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:right:width" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:left:width:carriageway" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:right:width:carriageway" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:left:offset" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="parking:lane:right:offset" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
    <constraint field="error_output_2" notnull_strength="0" unique_strength="0" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="highway" exp="" desc=""/>
    <constraint field="highway:name" exp="" desc=""/>
    <constraint field="highway:width_proc" exp="" desc=""/>
    <constraint field="highway:width_proc:effective" exp="" desc=""/>
    <constraint field="error_output" exp="" desc=""/>
    <constraint field="parking" exp="" desc=""/>
    <constraint field="position" exp="" desc=""/>
    <constraint field="condition" exp="" desc=""/>
    <constraint field="condition:other" exp="" desc=""/>
    <constraint field="condition:other:time" exp="" desc=""/>
    <constraint field="maxstay" exp="" desc=""/>
    <constraint field="capacity" exp="" desc=""/>
    <constraint field="width" exp="" desc=""/>
    <constraint field="offset" exp="" desc=""/>
    <constraint field="id_2" exp="" desc=""/>
    <constraint field="highway_2" exp="" desc=""/>
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
    <constraint field="error_output_2" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column width="-1" name="id" type="field" hidden="0"/>
      <column width="-1" name="highway" type="field" hidden="0"/>
      <column width="-1" name="highway:name" type="field" hidden="0"/>
      <column width="-1" name="highway:width_proc" type="field" hidden="0"/>
      <column width="-1" name="highway:width_proc:effective" type="field" hidden="0"/>
      <column width="-1" name="error_output" type="field" hidden="0"/>
      <column width="-1" name="parking" type="field" hidden="0"/>
      <column width="-1" name="position" type="field" hidden="0"/>
      <column width="-1" name="condition" type="field" hidden="0"/>
      <column width="-1" name="condition:other" type="field" hidden="0"/>
      <column width="-1" name="condition:other:time" type="field" hidden="0"/>
      <column width="-1" name="maxstay" type="field" hidden="0"/>
      <column width="-1" name="capacity" type="field" hidden="0"/>
      <column width="-1" name="width" type="field" hidden="0"/>
      <column width="-1" name="offset" type="field" hidden="0"/>
      <column width="-1" name="id_2" type="field" hidden="0"/>
      <column width="-1" name="highway_2" type="field" hidden="0"/>
      <column width="-1" name="name" type="field" hidden="0"/>
      <column width="-1" name="surface" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:left" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:right" type="field" hidden="0"/>
      <column width="-1" name="width_proc" type="field" hidden="0"/>
      <column width="-1" name="width_proc:effective" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:left:position" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:right:position" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:left:width" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:right:width" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:left:width:carriageway" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:right:width:carriageway" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:left:offset" type="field" hidden="0"/>
      <column width="-1" name="parking:lane:right:offset" type="field" hidden="0"/>
      <column width="-1" name="error_output_2" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
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
    <field name="capacity" editable="1"/>
    <field name="condition" editable="1"/>
    <field name="condition:other" editable="1"/>
    <field name="condition:other:time" editable="1"/>
    <field name="error_output" editable="1"/>
    <field name="error_output_2" editable="1"/>
    <field name="highway" editable="1"/>
    <field name="highway:name" editable="1"/>
    <field name="highway:width_proc" editable="1"/>
    <field name="highway:width_proc:effective" editable="1"/>
    <field name="highway_2" editable="1"/>
    <field name="id" editable="1"/>
    <field name="id_2" editable="1"/>
    <field name="maxstay" editable="1"/>
    <field name="name" editable="1"/>
    <field name="offset" editable="1"/>
    <field name="parking" editable="1"/>
    <field name="parking:lane:left" editable="1"/>
    <field name="parking:lane:left:offset" editable="1"/>
    <field name="parking:lane:left:position" editable="1"/>
    <field name="parking:lane:left:width" editable="1"/>
    <field name="parking:lane:left:width:carriageway" editable="1"/>
    <field name="parking:lane:right" editable="1"/>
    <field name="parking:lane:right:offset" editable="1"/>
    <field name="parking:lane:right:position" editable="1"/>
    <field name="parking:lane:right:width" editable="1"/>
    <field name="parking:lane:right:width:carriageway" editable="1"/>
    <field name="position" editable="1"/>
    <field name="surface" editable="1"/>
    <field name="width" editable="1"/>
    <field name="width_proc" editable="1"/>
    <field name="width_proc:effective" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="capacity"/>
    <field labelOnTop="0" name="condition"/>
    <field labelOnTop="0" name="condition:other"/>
    <field labelOnTop="0" name="condition:other:time"/>
    <field labelOnTop="0" name="error_output"/>
    <field labelOnTop="0" name="error_output_2"/>
    <field labelOnTop="0" name="highway"/>
    <field labelOnTop="0" name="highway:name"/>
    <field labelOnTop="0" name="highway:width_proc"/>
    <field labelOnTop="0" name="highway:width_proc:effective"/>
    <field labelOnTop="0" name="highway_2"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="id_2"/>
    <field labelOnTop="0" name="maxstay"/>
    <field labelOnTop="0" name="name"/>
    <field labelOnTop="0" name="offset"/>
    <field labelOnTop="0" name="parking"/>
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
    <field labelOnTop="0" name="position"/>
    <field labelOnTop="0" name="surface"/>
    <field labelOnTop="0" name="width"/>
    <field labelOnTop="0" name="width_proc"/>
    <field labelOnTop="0" name="width_proc:effective"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"highway:name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
