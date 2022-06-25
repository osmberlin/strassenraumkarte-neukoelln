<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" maxScale="0" minScale="100000000" simplifyLocal="1" readOnly="0" simplifyDrawingTol="1" styleCategories="AllStyleCategories" simplifyDrawingHints="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" version="3.16.3-Hannover" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startExpression="" endExpression="" fixedDuration="0" durationField="" accumulate="0" startField="" mode="0" endField="" durationUnit="min" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="RuleRenderer" enableorderby="0" symbollevels="0" forceraster="0">
    <rules key="{9a32b539-a6a1-4f67-97af-0353599c49e9}">
      <rule label="no parking" key="{7f6f2d4e-ad8c-44e6-a815-ffb0bc4af652}" filter="&quot;parking&quot; = 'no'" symbol="0"/>
      <rule label="separate parking" key="{bc541622-003a-4318-9f51-3a2d8a8d44c0}" filter="&quot;parking&quot; = 'separate'" symbol="1"/>
      <rule label="unknown parking" key="{7e35ce32-1c62-48d8-ad1d-d263bcb7ce66}" filter="&quot;parking&quot; != 'separate' and &quot;parking&quot; != 'no'" symbol="2"/>
    </rules>
    <symbols>
      <symbol alpha="1" name="0" clip_to_extent="1" type="line" force_rhr="0">
        <layer locked="0" class="MarkerLine" pass="0" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@0@0" clip_to_extent="1" type="marker" force_rhr="0">
            <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
              <prop k="angle" v="45"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="cross_fill"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="no"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="RenderMetersInMapUnits"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="1" clip_to_extent="1" type="line" force_rhr="0">
        <layer locked="0" class="MarkerLine" pass="0" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@1@0" clip_to_extent="1" type="marker" force_rhr="0">
            <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
              <prop k="angle" v="180"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="equilateral_triangle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="no"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="RenderMetersInMapUnits"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" name="2" clip_to_extent="1" type="line" force_rhr="0">
        <layer locked="0" class="MarkerLine" pass="0" enabled="1">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="RenderMetersInMapUnits"/>
          <prop k="placement" v="interval"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol alpha="1" name="@2@0" clip_to_extent="1" type="marker" force_rhr="0">
            <layer locked="0" class="FontMarker" pass="0" enabled="1">
              <prop k="angle" v="180"/>
              <prop k="chr" v="?"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="font" v="Arial"/>
              <prop k="font_style" v="Standard"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="size" v="3"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="RenderMetersInMapUnits"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties"/>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property value="false" key="OnConvertFormatRegeneratePrimaryKey"/>
    <property key="dualview/previewExpressions">
      <value>"highway:name"</value>
    </property>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory diagramOrientation="Up" backgroundAlpha="255" backgroundColor="#ffffff" opacity="1" maxScaleDenominator="1e+8" height="15" lineSizeType="MM" width="15" direction="0" labelPlacementMethod="XHeight" spacing="5" spacingUnitScale="3x:0,0,0,0,0,0" sizeType="MM" barWidth="5" penAlpha="255" minScaleDenominator="0" showAxis="1" enabled="0" minimumSize="0" rotationOffset="270" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" spacingUnit="MM" penColor="#000000" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area">
      <fontProperties description="Cantarell,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
      <axisSymbol>
        <symbol alpha="1" name="" clip_to_extent="1" type="line" force_rhr="0">
          <layer locked="0" class="SimpleLine" pass="0" enabled="1">
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
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
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
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
  <DiagramLayerSettings obstacle="0" priority="0" zIndex="0" linePlacementFlags="18" dist="0" showAll="1" placement="2">
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
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="highway:width_proc:effective" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="error_output" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="side" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="parking" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orientation" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="position" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="condition:other:time" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="vehicles" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="maxstay" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="source:capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="offset" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="layer" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="path" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="" field="highway" index="1"/>
    <alias name="" field="highway:name" index="2"/>
    <alias name="" field="highway:width_proc" index="3"/>
    <alias name="" field="highway:width_proc:effective" index="4"/>
    <alias name="" field="error_output" index="5"/>
    <alias name="" field="side" index="6"/>
    <alias name="" field="parking" index="7"/>
    <alias name="" field="orientation" index="8"/>
    <alias name="" field="position" index="9"/>
    <alias name="" field="condition" index="10"/>
    <alias name="" field="condition:other" index="11"/>
    <alias name="" field="condition:other:time" index="12"/>
    <alias name="" field="vehicles" index="13"/>
    <alias name="" field="maxstay" index="14"/>
    <alias name="" field="capacity" index="15"/>
    <alias name="" field="source:capacity" index="16"/>
    <alias name="" field="width" index="17"/>
    <alias name="" field="offset" index="18"/>
    <alias name="" field="layer" index="19"/>
    <alias name="" field="path" index="20"/>
  </aliases>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="highway" expression="" applyOnUpdate="0"/>
    <default field="highway:name" expression="" applyOnUpdate="0"/>
    <default field="highway:width_proc" expression="" applyOnUpdate="0"/>
    <default field="highway:width_proc:effective" expression="" applyOnUpdate="0"/>
    <default field="error_output" expression="" applyOnUpdate="0"/>
    <default field="side" expression="" applyOnUpdate="0"/>
    <default field="parking" expression="" applyOnUpdate="0"/>
    <default field="orientation" expression="" applyOnUpdate="0"/>
    <default field="position" expression="" applyOnUpdate="0"/>
    <default field="condition" expression="" applyOnUpdate="0"/>
    <default field="condition:other" expression="" applyOnUpdate="0"/>
    <default field="condition:other:time" expression="" applyOnUpdate="0"/>
    <default field="vehicles" expression="" applyOnUpdate="0"/>
    <default field="maxstay" expression="" applyOnUpdate="0"/>
    <default field="capacity" expression="" applyOnUpdate="0"/>
    <default field="source:capacity" expression="" applyOnUpdate="0"/>
    <default field="width" expression="" applyOnUpdate="0"/>
    <default field="offset" expression="" applyOnUpdate="0"/>
    <default field="layer" expression="" applyOnUpdate="0"/>
    <default field="path" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" constraints="0" field="id" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="highway" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="highway:name" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="highway:width_proc" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="highway:width_proc:effective" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="error_output" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="side" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="parking" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="orientation" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="position" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="condition" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="condition:other" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="condition:other:time" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="vehicles" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="maxstay" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="capacity" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="source:capacity" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="width" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="offset" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="layer" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" constraints="0" field="path" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="highway" exp=""/>
    <constraint desc="" field="highway:name" exp=""/>
    <constraint desc="" field="highway:width_proc" exp=""/>
    <constraint desc="" field="highway:width_proc:effective" exp=""/>
    <constraint desc="" field="error_output" exp=""/>
    <constraint desc="" field="side" exp=""/>
    <constraint desc="" field="parking" exp=""/>
    <constraint desc="" field="orientation" exp=""/>
    <constraint desc="" field="position" exp=""/>
    <constraint desc="" field="condition" exp=""/>
    <constraint desc="" field="condition:other" exp=""/>
    <constraint desc="" field="condition:other:time" exp=""/>
    <constraint desc="" field="vehicles" exp=""/>
    <constraint desc="" field="maxstay" exp=""/>
    <constraint desc="" field="capacity" exp=""/>
    <constraint desc="" field="source:capacity" exp=""/>
    <constraint desc="" field="width" exp=""/>
    <constraint desc="" field="offset" exp=""/>
    <constraint desc="" field="layer" exp=""/>
    <constraint desc="" field="path" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;parking&quot;" sortOrder="0">
    <columns>
      <column name="id" width="-1" type="field" hidden="0"/>
      <column name="highway" width="-1" type="field" hidden="0"/>
      <column name="highway:name" width="-1" type="field" hidden="0"/>
      <column name="highway:width_proc" width="-1" type="field" hidden="0"/>
      <column name="highway:width_proc:effective" width="-1" type="field" hidden="0"/>
      <column name="error_output" width="-1" type="field" hidden="0"/>
      <column name="parking" width="-1" type="field" hidden="0"/>
      <column name="orientation" width="-1" type="field" hidden="0"/>
      <column name="position" width="-1" type="field" hidden="0"/>
      <column name="condition" width="-1" type="field" hidden="0"/>
      <column name="condition:other" width="-1" type="field" hidden="0"/>
      <column name="condition:other:time" width="-1" type="field" hidden="0"/>
      <column name="vehicles" width="-1" type="field" hidden="0"/>
      <column name="maxstay" width="-1" type="field" hidden="0"/>
      <column name="capacity" width="-1" type="field" hidden="0"/>
      <column name="source:capacity" width="-1" type="field" hidden="0"/>
      <column name="width" width="-1" type="field" hidden="0"/>
      <column name="offset" width="-1" type="field" hidden="0"/>
      <column name="layer" width="-1" type="field" hidden="0"/>
      <column name="path" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
      <column name="side" width="-1" type="field" hidden="0"/>
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
    <field name="highway" editable="1"/>
    <field name="highway:name" editable="1"/>
    <field name="highway:width_proc" editable="1"/>
    <field name="highway:width_proc:effective" editable="1"/>
    <field name="id" editable="1"/>
    <field name="layer" editable="1"/>
    <field name="maxstay" editable="1"/>
    <field name="offset" editable="1"/>
    <field name="orientation" editable="1"/>
    <field name="parking" editable="1"/>
    <field name="path" editable="1"/>
    <field name="position" editable="1"/>
    <field name="side" editable="1"/>
    <field name="source:capacity" editable="1"/>
    <field name="vehicles" editable="1"/>
    <field name="width" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="capacity" labelOnTop="0"/>
    <field name="condition" labelOnTop="0"/>
    <field name="condition:other" labelOnTop="0"/>
    <field name="condition:other:time" labelOnTop="0"/>
    <field name="error_output" labelOnTop="0"/>
    <field name="highway" labelOnTop="0"/>
    <field name="highway:name" labelOnTop="0"/>
    <field name="highway:width_proc" labelOnTop="0"/>
    <field name="highway:width_proc:effective" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="layer" labelOnTop="0"/>
    <field name="maxstay" labelOnTop="0"/>
    <field name="offset" labelOnTop="0"/>
    <field name="orientation" labelOnTop="0"/>
    <field name="parking" labelOnTop="0"/>
    <field name="path" labelOnTop="0"/>
    <field name="position" labelOnTop="0"/>
    <field name="side" labelOnTop="0"/>
    <field name="source:capacity" labelOnTop="0"/>
    <field name="vehicles" labelOnTop="0"/>
    <field name="width" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"highway:name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
