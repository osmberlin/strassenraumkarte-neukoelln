<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="1" simplifyAlgorithm="0" version="3.16.3-Hannover" minScale="100000000" styleCategories="AllStyleCategories" readOnly="0" simplifyLocal="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyDrawingTol="1" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal durationUnit="min" durationField="" endExpression="" fixedDuration="0" enabled="0" startExpression="" accumulate="0" endField="" mode="0" startField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" forceraster="0" enableorderby="0" type="RuleRenderer">
    <rules key="{803f935d-d6de-4386-8143-af55ce9070fe}">
      <rule symbol="0" key="{77c31a18-3b85-43ed-9ced-853f1c8c7389}" label="parallel on_street" filter="&quot;orientation&quot; = 'parallel' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule symbol="1" key="{dde9ac74-a9ea-4202-8779-fc7d314b2961}" label="parallel half_on_kerb" filter="&quot;orientation&quot; = 'parallel' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule symbol="2" key="{7ad919ba-f76a-4074-94b8-dc3f4ad60bfb}" label="parallel on_kerb/shoulder/street_side/lay_by" filter="&quot;orientation&quot; = 'parallel' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
      <rule symbol="3" key="{469dcfde-eeb7-4d8e-b3ca-f21c5dc77aad}" label="diagonal on_street" filter="&quot;orientation&quot; = 'diagonal' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule symbol="4" key="{ffa64ff1-13ff-4dcd-a7a5-6cad92c48063}" label="diagonal half_on_kerb" filter="&quot;orientation&quot; = 'diagonal' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule symbol="5" key="{c7e5b9c2-2e94-4ac0-87b7-7cf0903d0507}" label="diagonal on_kerb/shoulder/street_side/lay_by" filter="&quot;orientation&quot; = 'diagonal' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
      <rule symbol="6" key="{2cc6da87-6460-4565-9d0a-1f9463f535bb}" label="perpendicular on_street" filter="&quot;orientation&quot; = 'perpendicular' AND ((&quot;position&quot; != 'half_on_kerb' AND &quot;position&quot; != 'on_kerb' AND &quot;position&quot; != 'shoulder' AND &quot;position&quot; != 'street_side' AND &quot;position&quot; != 'lay_by') OR &quot;position&quot; IS NULL)"/>
      <rule symbol="7" key="{2cc6da87-6460-4565-9d0a-1f9463f535bb}" label="perpendicular half_on_kerb" filter="&quot;orientation&quot; = 'perpendicular' AND &quot;position&quot; = 'half_on_kerb'"/>
      <rule symbol="8" key="{1387d40f-c62f-417f-a213-7442061b9203}" label="perpendicular on_kerb/shoulder/street_side/lay_by" filter="&quot;orientation&quot; = 'perpendicular' AND (&quot;position&quot; = 'on_kerb' OR &quot;position&quot; = 'shoulder' OR &quot;position&quot; = 'street_side' OR &quot;position&quot; = 'lay_by')"/>
    </rules>
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="0" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="-1.1"/>
          <prop k="offset_along_line" v="2.2"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@0@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="1" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="1.1"/>
          <prop k="offset_along_line" v="2.2"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@1@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="1.1"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="2" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="90"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="5.2"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="-1.1"/>
          <prop k="offset_along_line" v="2.2"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@2@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="-2.2"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="offset" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="if(&quot;side&quot; = 'separate', 0, -2.2)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="3" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="324"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="-2.2"/>
          <prop k="offset_along_line" v="3.1"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@3@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="4" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="144"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="3.1"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@4@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="5" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="144"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="3.1"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MapUnit"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="3.1"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@5@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="31,12,173,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="-3.1"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="offset" type="Map">
                      <Option value="true" name="active" type="bool"/>
                      <Option value="if(&quot;side&quot; = 'separate', 0, -3.1)" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
                  <Option value="collection" name="type" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="6" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="-2.2"/>
          <prop k="offset_along_line" v="1.1"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@6@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="7" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="1.1"/>
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
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@7@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
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
        </layer>
      </symbol>
      <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="8" type="line">
        <layer class="HashLine" enabled="1" locked="0" pass="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="hash_angle" v="0"/>
          <prop k="hash_length" v="2.2"/>
          <prop k="hash_length_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="hash_length_unit" v="RenderMetersInMapUnits"/>
          <prop k="interval" v="2.5"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="RenderMetersInMapUnits"/>
          <prop k="offset" v="2.2"/>
          <prop k="offset_along_line" v="1.1"/>
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
              <Option name="properties" type="Map">
                <Option name="offset" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="if(&quot;side&quot; = 'separate', -2.2, 2.2)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="@8@0" type="line">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="RenderMetersInMapUnits"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="6,34,172,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.8"/>
              <prop k="line_width_unit" v="RenderMetersInMapUnits"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="RenderMetersInMapUnits"/>
              <prop k="ring_filter" v="0"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString"/>
                  <Option name="properties" type="Map">
                    <Option name="offset" type="Map">
                      <Option value="false" name="active" type="bool"/>
                      <Option value="" name="expression" type="QString"/>
                      <Option value="3" name="type" type="int"/>
                    </Option>
                  </Option>
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
    <property key="dualview/previewExpressions">
      <value>"highway:name"</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory width="15" maxScaleDenominator="1e+8" sizeScale="3x:0,0,0,0,0,0" spacingUnit="MM" barWidth="5" enabled="0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" sizeType="MM" backgroundColor="#ffffff" lineSizeType="MM" penWidth="0" rotationOffset="270" showAxis="1" labelPlacementMethod="XHeight" spacing="5" scaleDependency="Area" minimumSize="0" penAlpha="255" scaleBasedVisibility="0" direction="0" height="15" spacingUnitScale="3x:0,0,0,0,0,0" minScaleDenominator="0" opacity="1" penColor="#000000">
      <fontProperties description="Cantarell,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
      <axisSymbol>
        <symbol clip_to_extent="1" force_rhr="0" alpha="1" name="" type="line">
          <layer class="SimpleLine" enabled="1" locked="0" pass="0">
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
  <DiagramLayerSettings placement="2" zIndex="0" showAll="1" linePlacementFlags="18" priority="0" obstacle="0" dist="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="highway">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="highway:name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="highway:width_proc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="highway:width_proc:effective">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="error_output">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="side">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="parking">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="orientation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="position">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="condition">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="condition:other">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="condition:other:time">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="vehicles">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="maxstay">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="source:capacity">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="width">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="offset">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="layer">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="path">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="id" name=""/>
    <alias index="1" field="highway" name=""/>
    <alias index="2" field="highway:name" name=""/>
    <alias index="3" field="highway:width_proc" name=""/>
    <alias index="4" field="highway:width_proc:effective" name=""/>
    <alias index="5" field="error_output" name=""/>
    <alias index="6" field="side" name=""/>
    <alias index="7" field="parking" name=""/>
    <alias index="8" field="orientation" name=""/>
    <alias index="9" field="position" name=""/>
    <alias index="10" field="condition" name=""/>
    <alias index="11" field="condition:other" name=""/>
    <alias index="12" field="condition:other:time" name=""/>
    <alias index="13" field="vehicles" name=""/>
    <alias index="14" field="maxstay" name=""/>
    <alias index="15" field="capacity" name=""/>
    <alias index="16" field="source:capacity" name=""/>
    <alias index="17" field="width" name=""/>
    <alias index="18" field="offset" name=""/>
    <alias index="19" field="layer" name=""/>
    <alias index="20" field="path" name=""/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="highway" expression=""/>
    <default applyOnUpdate="0" field="highway:name" expression=""/>
    <default applyOnUpdate="0" field="highway:width_proc" expression=""/>
    <default applyOnUpdate="0" field="highway:width_proc:effective" expression=""/>
    <default applyOnUpdate="0" field="error_output" expression=""/>
    <default applyOnUpdate="0" field="side" expression=""/>
    <default applyOnUpdate="0" field="parking" expression=""/>
    <default applyOnUpdate="0" field="orientation" expression=""/>
    <default applyOnUpdate="0" field="position" expression=""/>
    <default applyOnUpdate="0" field="condition" expression=""/>
    <default applyOnUpdate="0" field="condition:other" expression=""/>
    <default applyOnUpdate="0" field="condition:other:time" expression=""/>
    <default applyOnUpdate="0" field="vehicles" expression=""/>
    <default applyOnUpdate="0" field="maxstay" expression=""/>
    <default applyOnUpdate="0" field="capacity" expression=""/>
    <default applyOnUpdate="0" field="source:capacity" expression=""/>
    <default applyOnUpdate="0" field="width" expression=""/>
    <default applyOnUpdate="0" field="offset" expression=""/>
    <default applyOnUpdate="0" field="layer" expression=""/>
    <default applyOnUpdate="0" field="path" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="id" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="highway" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="highway:name" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="highway:width_proc" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="highway:width_proc:effective" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="error_output" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="side" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="parking" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="orientation" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="position" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="condition" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="condition:other" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="condition:other:time" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="vehicles" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="maxstay" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="capacity" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="source:capacity" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="width" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="offset" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="layer" exp_strength="0" constraints="0" unique_strength="0"/>
    <constraint notnull_strength="0" field="path" exp_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="highway" desc=""/>
    <constraint exp="" field="highway:name" desc=""/>
    <constraint exp="" field="highway:width_proc" desc=""/>
    <constraint exp="" field="highway:width_proc:effective" desc=""/>
    <constraint exp="" field="error_output" desc=""/>
    <constraint exp="" field="side" desc=""/>
    <constraint exp="" field="parking" desc=""/>
    <constraint exp="" field="orientation" desc=""/>
    <constraint exp="" field="position" desc=""/>
    <constraint exp="" field="condition" desc=""/>
    <constraint exp="" field="condition:other" desc=""/>
    <constraint exp="" field="condition:other:time" desc=""/>
    <constraint exp="" field="vehicles" desc=""/>
    <constraint exp="" field="maxstay" desc=""/>
    <constraint exp="" field="capacity" desc=""/>
    <constraint exp="" field="source:capacity" desc=""/>
    <constraint exp="" field="width" desc=""/>
    <constraint exp="" field="offset" desc=""/>
    <constraint exp="" field="layer" desc=""/>
    <constraint exp="" field="path" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;id&quot;" sortOrder="0">
    <columns>
      <column width="271" hidden="0" name="id" type="field"/>
      <column width="-1" hidden="0" name="highway" type="field"/>
      <column width="-1" hidden="0" name="highway:name" type="field"/>
      <column width="-1" hidden="0" name="error_output" type="field"/>
      <column width="-1" hidden="0" name="parking" type="field"/>
      <column width="-1" hidden="0" name="position" type="field"/>
      <column width="-1" hidden="0" name="condition" type="field"/>
      <column width="-1" hidden="0" name="condition:other" type="field"/>
      <column width="-1" hidden="0" name="condition:other:time" type="field"/>
      <column width="-1" hidden="0" name="maxstay" type="field"/>
      <column width="-1" hidden="0" name="capacity" type="field"/>
      <column width="-1" hidden="0" name="width" type="field"/>
      <column width="-1" hidden="0" name="offset" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" hidden="0" name="highway:width_proc" type="field"/>
      <column width="-1" hidden="0" name="highway:width_proc:effective" type="field"/>
      <column width="-1" hidden="0" name="orientation" type="field"/>
      <column width="-1" hidden="0" name="source:capacity" type="field"/>
      <column width="-1" hidden="0" name="layer" type="field"/>
      <column width="-1" hidden="0" name="path" type="field"/>
      <column width="-1" hidden="0" name="vehicles" type="field"/>
      <column width="-1" hidden="0" name="side" type="field"/>
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
    <field editable="1" name="capacity"/>
    <field editable="1" name="condition"/>
    <field editable="1" name="condition:other"/>
    <field editable="1" name="condition:other:time"/>
    <field editable="1" name="error_output"/>
    <field editable="1" name="highway"/>
    <field editable="1" name="highway:name"/>
    <field editable="1" name="highway:width"/>
    <field editable="1" name="highway:width:effective"/>
    <field editable="1" name="highway:width_proc"/>
    <field editable="1" name="highway:width_proc:effective"/>
    <field editable="1" name="id"/>
    <field editable="1" name="layer"/>
    <field editable="1" name="maxstay"/>
    <field editable="1" name="offset"/>
    <field editable="1" name="orientation"/>
    <field editable="1" name="parking"/>
    <field editable="1" name="path"/>
    <field editable="1" name="position"/>
    <field editable="1" name="side"/>
    <field editable="1" name="source:capacity"/>
    <field editable="1" name="vehicles"/>
    <field editable="1" name="width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="capacity"/>
    <field labelOnTop="0" name="condition"/>
    <field labelOnTop="0" name="condition:other"/>
    <field labelOnTop="0" name="condition:other:time"/>
    <field labelOnTop="0" name="error_output"/>
    <field labelOnTop="0" name="highway"/>
    <field labelOnTop="0" name="highway:name"/>
    <field labelOnTop="0" name="highway:width"/>
    <field labelOnTop="0" name="highway:width:effective"/>
    <field labelOnTop="0" name="highway:width_proc"/>
    <field labelOnTop="0" name="highway:width_proc:effective"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="layer"/>
    <field labelOnTop="0" name="maxstay"/>
    <field labelOnTop="0" name="offset"/>
    <field labelOnTop="0" name="orientation"/>
    <field labelOnTop="0" name="parking"/>
    <field labelOnTop="0" name="path"/>
    <field labelOnTop="0" name="position"/>
    <field labelOnTop="0" name="side"/>
    <field labelOnTop="0" name="source:capacity"/>
    <field labelOnTop="0" name="vehicles"/>
    <field labelOnTop="0" name="width"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"highway:name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
